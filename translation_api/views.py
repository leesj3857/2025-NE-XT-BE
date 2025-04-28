from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.management import call_command
from django.conf import settings
from .models import Category, RegionName, CategoryLog, RegionLog, PlaceInfo, PlaceLog, User, EmailVerification
import requests
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError
import re
from serpapi import GoogleSearch
from django.contrib.auth import authenticate, get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import secrets

DEEPL_URL = 'https://api-free.deepl.com/v2/translate'
DEEPL_AUTH_KEY = settings.DEEPL_API_KEY

        
@api_view(['POST'])
def run_migrate(request):
    try:
        # 마이그레이션 파일 생성 (필요 시)
        call_command('makemigrations', 'translation_api', interactive=False)

        # migrate 수행 (새로운 테이블만 생성)
        call_command('migrate', 'translation_api', interactive=False)

        return Response({'message': 'Migration applied successfully'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


    

def deepl_translate(text: str, source_lang: str, target_lang: str) -> str:
    """ Deepl API 호출 함수 """
    try:
        res = requests.post(
            DEEPL_URL,
            data={
                'text': text,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'auth_key': DEEPL_AUTH_KEY,
            }
        )
        res.raise_for_status()
        return res.json()['translations'][0]['text']
    except Exception as e:
        raise RuntimeError(f'DeepL translation failed: {str(e)}')


@api_view(['POST'])
def translate_category(request):
    """ 한글 카테고리를 영어로 번역 """
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Missing text field'}, status=400)
    
    CategoryLog.objects.create(korean=text)
    
    try:
        category = Category.objects.get(korean=text)
        return Response({'translated_text': category.english})
    except Category.DoesNotExist:
        pass

    try:
        translated = deepl_translate(text, source_lang='KO', target_lang='EN')
        Category.objects.create(korean=text, english=translated)
        return Response({'translated_text': translated})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
def translate_region_to_korean(request):
    """ 영어 지역명을 한글로 번역 """
    text = request.data.get('text')
    if not text:
        return Response({'error': 'Missing text field'}, status=400)
    
    RegionLog.objects.create(english=text)
    
    try:
        region = RegionName.objects.get(english=text)
        return Response({'translated_text': region.korean})
    except RegionName.DoesNotExist:
        pass

    try:
        translated = deepl_translate(text, source_lang='EN', target_lang='KO')
        RegionName.objects.create(korean=translated, english=text)
        return Response({'translated_text': translated})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def get_place_info(request):
    name = request.data.get('name')
    address = request.data.get('address')

    if not name or not address:
        return Response({'error': 'Missing name or address'}, status=400)

    # 로그 저장
    PlaceLog.objects.create(name=name, address=address)

    try:
        # DB에 이미 존재하는지 확인
        place = PlaceInfo.objects.get(name=name, address=address)
        return Response({
            "title": place.title,
            "category": place.category,
            "address": place.address,
            "description": place.description,
            "menu_or_ticket_info": place.menu_or_ticket_info,
            "price": place.price,
            "translated_reviews": place.translated_reviews,
        })

    except PlaceInfo.DoesNotExist:
        # SERP API 호출
        query = f"{name} {address}"
        params = {
            "engine": "google",
            "q": query,
            "type": "search",
            "google_domain": "google.co.kr",
            "hl": "ko",
            "gl": "kr",
            "api_key": settings.SERPAPI_KEY
        }

        try:
            search = GoogleSearch(params)
            result = search.get_dict()

            # 변경된 구조: place_info와 reviews 따로 추출
            place_info = result.get("place_info", {})
            reviews = result.get("reviews", [])

            # 한국어 후기만 추출하고 번역
            korean_reviews = [r["snippet"] for r in reviews if re.search(r"[가-힣]", r.get("snippet", ""))]
            translated_reviews = [
                deepl_translate(text, source_lang="KO", target_lang="EN")
                for text in korean_reviews
            ]

            # DB 저장
            place = PlaceInfo.objects.create(
                name=name,
                address=address,
                title=place_info.get("title"),
                category=place_info.get("type"),
                description=place_info.get("description"),
                menu_or_ticket_info=place_info.get("attributes", {}),
                price=place_info.get("price"),
                translated_reviews=translated_reviews,
            )

            return Response({
                "title": place.title,
                "category": place.category,
                "address": place.address,
                "description": place.description,
                "menu_or_ticket_info": place.menu_or_ticket_info,
                "price": place.price,
                "translated_reviews": place.translated_reviews,
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
        

User = get_user_model()

@api_view(['POST'])
def register(request):
    email = request.data.get('email')
    name = request.data.get('name')
    password = request.data.get('password')
    token = request.data.get('token')

    if not all([email, name, password, token]):
        return Response({'error': '모든 정보를 입력해주세요.'}, status=400)

    try:
        record = EmailVerification.objects.filter(email=email, purpose='register').latest('created_at')
    except EmailVerification.DoesNotExist:
        return Response({'error': '이메일 인증 기록이 없습니다.'}, status=404)

    if record.token != token:
        return Response({'error': '유효하지 않은 토큰입니다.'}, status=400)

    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # ✅ 회원가입 완료 후 인증 기록 삭제
        record.delete()
        return Response({"message": "회원가입 성공!"})
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "로그인 성공",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user_id": user.id,
                "name": user.name,
            })
        return Response({"error": "이메일 또는 비밀번호가 틀렸습니다."}, status=400)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def check_email_duplicate(request):
    email = request.data.get('email')
    if User.objects.filter(email=email).exists():
        return Response({"exists": True})
    return Response({"exists": False})

@api_view(['POST'])
def send_verification_code(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': '이메일이 필요합니다.'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': '이미 가입된 이메일입니다.'}, status=409)

    code = str(random.randint(100000, 999999))

    EmailVerification.objects.filter(email=email, purpose='register').delete()
    EmailVerification.objects.create(email=email, code=code, purpose='register')

    subject = '[KOREAT] 회원가입 인증번호 안내'
    body = f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2 style="color: #4CAF50;">KOREAT 회원가입 인증번호</h2>
            <p>아래 인증번호를 5분 이내에 입력해주세요.</p>
            <div style="font-size: 30px; font-weight: bold; margin: 20px 0;">{code}</div>
            <p>감사합니다.</p>
        </body>
    </html>
    """

    try:
        message = EmailMultiAlternatives(subject=subject, body='회원가입 인증번호입니다.', to=[email])
        message.attach_alternative(body, "text/html")
        message.send()
        return Response({'message': '인증번호가 이메일로 전송되었습니다.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def verify_email_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({'error': '이메일과 인증번호를 입력해주세요.'}, status=400)

    try:
        record = EmailVerification.objects.filter(email=email, purpose='register').latest('created_at')
    except EmailVerification.DoesNotExist:
        return Response({'error': '인증 요청 기록이 없습니다.'}, status=404)

    if record.is_expired():
        return Response({'error': '인증번호가 만료되었습니다.'}, status=400)

    if record.code != code:
        return Response({'error': '인증번호가 일치하지 않습니다.'}, status=400)

    # ✅ 인증 성공: 일회용 토큰 발급
    one_time_token = secrets.token_urlsafe(32)
    record.token = one_time_token
    record.save()

    return Response({'message': '이메일 인증 성공', 'token': one_time_token})

# 1. 비밀번호 재설정용 인증번호 전송
@api_view(['POST'])
def send_password_reset_code(request):
    email = request.data.get('email')
    if not User.objects.filter(email=email).exists():
        return Response({'error': '해당 이메일로 가입된 사용자가 없습니다.'}, status=404)

    code = str(random.randint(100000, 999999))

    EmailVerification.objects.filter(email=email, purpose='reset').delete()
    EmailVerification.objects.create(email=email, code=code, purpose='reset')

    subject = '[KOREAT] 비밀번호 재설정 인증번호 안내'
    body = f"""
    <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2 style="color: #FF5722;">KOREAT 비밀번호 재설정 인증번호</h2>
            <p>아래 인증번호를 5분 이내에 입력해주세요.</p>
            <div style="font-size: 30px; font-weight: bold; margin: 20px 0;">{code}</div>
            <p>감사합니다.</p>
        </body>
    </html>
    """

    try:
        message = EmailMultiAlternatives(subject=subject, body='비밀번호 재설정 인증번호입니다.', to=[email])
        message.attach_alternative(body, "text/html")
        message.send()
        return Response({'message': '인증번호가 이메일로 전송되었습니다.'})
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# 2. 인증번호 인증만 하는 API
@api_view(['POST'])
def verify_reset_code(request):
    email = request.data.get('email')
    code = request.data.get('code')

    if not email or not code:
        return Response({'error': '이메일과 인증번호를 입력해주세요.'}, status=400)

    try:
        record = EmailVerification.objects.filter(email=email, purpose='reset').latest('created_at')
    except EmailVerification.DoesNotExist:
        return Response({'error': '비밀번호 재설정 요청 기록이 없습니다.'}, status=404)

    if record.is_expired():
        return Response({'error': '인증번호가 만료되었습니다.'}, status=400)

    if record.code != code:
        return Response({'error': '인증번호가 일치하지 않습니다.'}, status=400)

    # ✅ 토큰 생성 및 저장
    one_time_token = secrets.token_urlsafe(32)
    record.token = one_time_token
    record.save()

    return Response({'message': '인증 성공', 'token': one_time_token})

# 3. 실제 비밀번호 변경 API
@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    if not all([email, token, new_password]):
        return Response({'error': '모든 정보를 입력해주세요.'}, status=400)

    try:
        record = EmailVerification.objects.filter(email=email, purpose='reset').latest('created_at')
    except EmailVerification.DoesNotExist:
        return Response({'error': '비밀번호 재설정 요청 기록이 없습니다.'}, status=404)

    # ✅ 토큰 일치 여부 확인
    if record.token != token:
        return Response({'error': '유효하지 않은 토큰입니다.'}, status=400)

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # ✅ 완료 후 인증 기록 삭제 (또는 token 필드만 삭제하고 레코드 남겨도 됨)
        record.delete()

        return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'})
    except User.DoesNotExist:
        return Response({'error': '사용자를 찾을 수 없습니다.'}, status=404)
