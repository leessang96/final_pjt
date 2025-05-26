
import requests
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search_nearby_banks(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radius = request.GET.get('radius', '1000')  # 기본 1km

    if not lat or not lng:
        return JsonResponse({'error': 'lat/lng is required'}, status=400)

    url = 'https://dapi.kakao.com/v2/local/search/category.json'
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }
    params = {
        'category_group_code': 'BK9',  # 은행 코드
        'x': lng,
        'y': lat,
        'radius': radius
    }

    res = requests.get(url, headers=headers, params=params)
    return JsonResponse(res.json())
