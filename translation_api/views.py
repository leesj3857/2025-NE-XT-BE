from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Category
import requests
from django.conf import settings

@api_view(['POST'])
def translate_category(request):
    text = request.data.get('text')

    if not text:
        return Response({'error': 'Missing text field'}, status=400)

    # ✅ 이미 DB에 존재하는 경우 바로 반환
    try:
        category = Category.objects.get(korean=text)
        return Response({'translated_text': category.english})
    except Category.DoesNotExist:
        pass

    # ✅ DeepL API로 번역
    deepl_url = 'https://api-free.deepl.com/v2/translate'
    data = {
        'text': text,
        'source_lang': 'KO',
        'target_lang': 'EN',
        'auth_key': settings.DEEPL_API_KEY,
    }
    response = requests.post(deepl_url, data=data)
    result = response.json()
    translated_text = result['translations'][0]['text']

    # ✅ 존재하지 않을 때만 저장
    Category.objects.create(korean=text, english=translated_text)

    return Response({'translated_text': translated_text})
