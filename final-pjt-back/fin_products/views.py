# fin_products/views.py

from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    TermDeposit, TermDepositOption,
    InstallmentSaving, InstallmentSavingOption
)
from .serializers import TermDepositSerializer, InstallmentSavingSerializer
import requests


### [1] 정기예금 저장용 API 호출 후 DB 저장 ###
@api_view(['GET', 'POST'])
def fetch_and_save_term_deposits(request):
    url = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    fin_groups = ["020000", "030300"]
    all_base = []
    all_option = []

    for group in fin_groups:
        page = 1
        while True:
            params = {
                "auth": settings.API_KEY,
                "topFinGrpNo": group,
                "pageNo": page,
            }
            res = requests.get(url, params=params)
            data = res.json()

            base_list = data.get("result", {}).get("baseList", [])
            option_list = data.get("result", {}).get("optionList", [])

            if not base_list:
                break

            all_base.extend(base_list)
            all_option.extend(option_list)
            page += 1

    for base in all_base:
        if TermDeposit.objects.filter(fin_prdt_cd=base["fin_prdt_cd"]).exists():
            continue

        product = TermDeposit.objects.create(
            fin_prdt_cd=base["fin_prdt_cd"],
            dcls_month=base["dcls_month"],
            fin_co_no=base["fin_co_no"],
            kor_co_nm=base["kor_co_nm"],
            fin_prdt_nm=base["fin_prdt_nm"],
            join_deny=base["join_deny"],
            join_member=base["join_member"],
            join_way=base["join_way"],
            spcl_cnd=base["spcl_cnd"],
            etc_note=base.get("etc_note", ""),
            mtrt_int=base.get("mtrt_int", "")
        )

        options = [
            TermDepositOption(
                product=product,
                save_trm=o["save_trm"],
                intr_rate_type_nm=o["intr_rate_type_nm"],
                intr_rate=o["intr_rate"],
                intr_rate2=o["intr_rate2"]
            )
            for o in all_option if o["fin_prdt_cd"] == base["fin_prdt_cd"]
        ]
        TermDepositOption.objects.bulk_create(options)

    return JsonResponse({"message": "정기예금 저장 완료", "count": len(all_base)})


### [2] 적금 저장용 ###
@api_view(['GET', 'POST'])
def fetch_and_save_saving_deposits(request):
    url = "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    fin_groups = ["020000", "030300"]
    all_base = []
    all_option = []

    for group in fin_groups:
        page = 1
        while True:
            params = {
                "auth": settings.API_KEY,
                "topFinGrpNo": group,
                "pageNo": page,
            }
            res = requests.get(url, params=params)
            data = res.json()

            base_list = data.get("result", {}).get("baseList", [])
            option_list = data.get("result", {}).get("optionList", [])

            if not base_list:
                break

            all_base.extend(base_list)
            all_option.extend(option_list)
            page += 1

    for base in all_base:
        if InstallmentSaving.objects.filter(fin_prdt_cd=base["fin_prdt_cd"]).exists():
            continue

        product = InstallmentSaving.objects.create(
            fin_prdt_cd=base["fin_prdt_cd"],
            dcls_month=base["dcls_month"],
            fin_co_no=base["fin_co_no"],
            kor_co_nm=base["kor_co_nm"],
            fin_prdt_nm=base["fin_prdt_nm"],
            join_deny=base["join_deny"],
            join_member=base["join_member"],
            join_way=base["join_way"],
            spcl_cnd=base["spcl_cnd"],
            etc_note=base.get("etc_note", ""),
            mtrt_int=base.get("mtrt_int", "")
        )

        options = [
            InstallmentSavingOption(
                product=product,
                save_trm=o["save_trm"],
                intr_rate_type_nm=o["intr_rate_type_nm"],
                intr_rate=o["intr_rate"],
                intr_rate2=o["intr_rate2"]
            )
            for o in all_option if o["fin_prdt_cd"] == base["fin_prdt_cd"]
        ]
        InstallmentSavingOption.objects.bulk_create(options)

    return JsonResponse({"message": "적금 저장 완료", "count": len(all_base)})


### [3] DB 조회용 (렌더링용) ###
@api_view(['GET'])
def get_term_deposits(request):
    deposits = TermDeposit.objects.prefetch_related('optionList').all()
    serializer = TermDepositSerializer(deposits, many=True)
    return Response({'result': serializer.data})


@api_view(['GET'])
def get_saving_deposits(request):
    savings = InstallmentSaving.objects.prefetch_related('optionList').all()
    serializer = InstallmentSavingSerializer(savings, many=True)
    return Response({'result': serializer.data})


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings

# import requests

# def term_deposits(request): # 정기 예금
#     url = "https://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
#     fin_groups = ["020000", "030300"]
#     all_base = []
#     all_option = []

#     for group in fin_groups:
#         page = 1
#         while True:
#             params = {
#                 "auth": settings.API_KEY,
#                 # "topFinGrpNo": "020000",    # 은행, 23일 기준 39개
#                 # "topFinGrpNo": "030200",    # 여신전문, 23일 기준 0개
#                 # "topFinGrpNo": "030300",    # 저축은행, 23일 기준 379개
#                 # "topFinGrpNo": "050000",    # 보험, 23일 기준 0개
#                 # "topFinGrpNo": "060000",    # 금융투자, 23일 기준 0개
#                 "topFinGrpNo": group,         # 418개 -> 랜더링되는 페이지는 42페이지 될 듯..?
#                 "pageNo": page,               
#             }
#             res = requests.get(url, params=params)
#             data = res.json()

#             base_list = data.get("result", {}).get("baseList", [])
#             option_list = data.get("result", {}).get("optionList", [])

#             if not base_list:
#                 break

#             all_base.extend(base_list)
#             all_option.extend(option_list)
#             page += 1    
    
#     # fin_prdt_cd 기준으로 optionList 병합
#     option_map = {}
#     for option in all_option:
#         code = option["fin_prdt_cd"]
#         if code not in option_map:
#             option_map[code] = []
#         option_map[code].append(option)

#     # baseList에 optionList 병합
#     cross_list = []
#     for base in all_base:
#         code = base["fin_prdt_cd"]
#         base["optionList"] = option_map.get(code, []) # 없으면 빈 리스트
#         cross_list.append(base)

#     return JsonResponse({"result": cross_list})

# def saving_deposits(request):                 # 적금   
#     url = "https://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
#     fin_groups = ["020000", "030300"]
#     all_base = []
#     all_option = []

#     for group in fin_groups:
#         page = 1
#         while True:
#             params = {
#                 "auth": settings.API_KEY,
#                 # "topFinGrpNo": "020000",    # 은행, 23일 기준 39개
#                 # "topFinGrpNo": "030200",    # 여신전문, 23일 기준 0개
#                 # "topFinGrpNo": "030300",    # 저축은행, 23일 기준 379개
#                 # "topFinGrpNo": "050000",    # 보험, 23일 기준 0개
#                 # "topFinGrpNo": "060000",    # 금융투자, 23일 기준 0개
#                 "topFinGrpNo": group,         # 418개 -> 랜더링되는 페이지는 42페이지 될 듯..?
#                 "pageNo": page,               
#             }
#             res = requests.get(url, params=params)
#             data = res.json()

#             base_list = data.get("result", {}).get("baseList", [])
#             option_list = data.get("result", {}).get("optionList", [])

#             if not base_list:
#                 break

#             all_base.extend(base_list)
#             all_option.extend(option_list)
#             page += 1    
    
#     # fin_prdt_cd 기준으로 optionList 병합
#     option_map = {}
#     for option in all_option:
#         code = option["fin_prdt_cd"]
#         if code not in option_map:
#             option_map[code] = []
#         option_map[code].append(option)

#     # baseList에 optionList 병합
#     cross_list = []
#     for base in all_base:
#         code = base["fin_prdt_cd"]
#         base["optionList"] = option_map.get(code, []) # 없으면 빈 리스트
#         cross_list.append(base)

#     return JsonResponse({"result": cross_list})



#     # 불러온 데이터 길이 확인하는 함수 
#     # for test_page in range(1, 4):
#     #     params = {
#     #         "auth": settings.API_KEY,
#     #         "topFinGrpNo": "020000",
#     #         "pageNo": test_page
#     #     }
#     #     res = requests.get(url, params=params)
#     #     data = res.json()
#     #     print(f"[TEST] page {test_page} - baseList: {len(data.get('result', {}).get('baseList', []))}")

# # # optionList 내부 데이터 정보
# #     {
# #   "dcls_month": "202505",           // 공시 기준 연월 (2025년 5월)
# #   "fin_co_no": "0010001",           // 금융회사 코드
# #   "fin_prdt_cd": "WR0001B",         // 금융상품 코드 (baseList와 연결 키)
# #   "intr_rate_type": "S",            // 금리 유형 코드: S=단리, M=복리
# #   "intr_rate_type_nm": "단리",      // 금리 유형 이름: 단리 or 복리
# #   "save_trm": "1",                  // 저축 기간 (단위: 개월)
# #   "intr_rate": 2.7,                 // 기본 이자율 (최소 보장 금리)
# #   "intr_rate2": 2.7                 // 최고 우대 이자율 (조건 만족 시)
# # }