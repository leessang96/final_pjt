from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

import requests

def term_deposits(request): # 정기 예금
    base_url = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {
        "auth": settings.API_KEY,
        "topFinGrpNo": "020000",
        "pageNo": 1
    }

    res = requests.get(base_url, params=params)
    data = res.json()

    return JsonResponse(data)

def saving_deposits(request):   # 적금   
    pass