from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.management import call_command
from django.conf import settings
from .models import Category, RegionName, CategoryLog, RegionLog, PlaceInfo, PlaceLog 
import requests
from django.db.utils import ProgrammingError, OperationalError
from django.db import IntegrityError
import re
from serpapi import GoogleSearch

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
            "engine": "google_maps",
            "q": query,
            "type": "search",
            "google_domain": "google.co.kr",
            "hl": "ko",
            "api_key": settings.SERPAPI_KEY
        }

        try:
            search = GoogleSearch(params)
            result = search.get_dict()
            place_info = result.get("place_results", {})
            reviews = place_info.get("reviews", [])

            # 한국어 후기만 추출하고 번역
            korean_reviews = [r["text"] for r in reviews if re.search(r"[가-힣]", r.get("text", ""))]
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
                menu_or_ticket_info=place_info.get("menu") if "menu" in place_info else place_info.get("attributes", {}),
                price=place_info.get("price_level"),
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
        