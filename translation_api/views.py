from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.management import call_command
from django.conf import settings
from .models import Category, RegionName, CategoryLog, RegionLog
import requests
from django.db.utils import ProgrammingError, OperationalError

DEEPL_URL = 'https://api-free.deepl.com/v2/translate'
DEEPL_AUTH_KEY = settings.DEEPL_API_KEY


@api_view(['POST'])
def run_migrate(request):
    """ DB 마이그레이션 수동 실행용 """
    try:
        call_command('makemigrations', interactive=False)
        call_command('migrate', interactive=False)
        return Response({'message': 'Migration completed successfully'})
    except (ProgrammingError, OperationalError) as db_error:
        return Response({'message': 'Migration partially completed or already applied', 'details': str(db_error)}, status=200)
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
