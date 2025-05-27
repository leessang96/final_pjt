import requests
import re
import operator
from functools import reduce
from django.db.models import Q
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import (
    TermDeposit, TermDepositOption,
    InstallmentSaving, InstallmentSavingOption,
)
from .serializers import TermDepositSerializer, InstallmentSavingSerializer


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

# -----------------------------

from traceback import format_exc

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_based_recommendation(request):
    try:
        user = request.user
        user_age = user.age or 0

        product_type = request.GET.get('product_type')
        if product_type not in ['term', 'saving']:
            return Response({"error": "올바르지 않은 product_type입니다."}, status=400)

        min_rate = float(request.GET.get('min_rate', 0))
        min_term = int(request.GET.get('min_term', 1))
        max_term = int(request.GET.get('max_term', 36))

        if min_rate < 0:
            return Response({"error": "최소 이자율은 0 이상이어야 합니다."}, status=400)
        if min_term > max_term:
            return Response({"error": "예치 최소 기간은 최대 기간보다 작거나 같아야 합니다."}, status=400)

        banking_type = request.GET.get('banking_type', '')
        preferred_banks = request.GET.get('preferred_banks', '').split(',')

        # 먼저 product_type에 따라 Model과 Serializer를 선택
        Model = TermDeposit if product_type == 'term' else InstallmentSaving
        Serializer = TermDepositSerializer if product_type == 'term' else InstallmentSavingSerializer

        # 그 다음 queryset 구성 시작
        queryset = Model.objects.filter(
            optionList__intr_rate__gte=min_rate,
        ).distinct()

        # 뱅킹 방식 필터 적용
        banking_keywords = {
            '인터넷': ['인터넷', '인터넷뱅킹', '비대면'],
            '모바일': ['모바일', '스마트폰', '스마트폰뱅킹', '모바일앱', '비대면'],
            '창구': ['창구', '영업점'],
        }

        if banking_type in banking_keywords:
            queryset = queryset.filter(
                reduce(operator.or_, [
                    Q(join_way__icontains=kw) for kw in banking_keywords[banking_type]
                ])
            )

        # 선호 은행 필터 적용
        if preferred_banks and preferred_banks != ['']:
            queryset = queryset.filter(
                reduce(operator.or_, [
                    Q(kor_co_nm__icontains=bank.strip()) for bank in preferred_banks
                ])
            )


        filtered = sorted(
            [
                p for p in queryset
                if is_age_eligible(p.join_member, user_age)
                and is_term_in_range(p, min_term, max_term)
                and get_max_rate_in_term(p, min_term, max_term) >= min_rate
            ],
            key=lambda p: (
                -get_max_rate_in_term(p, min_term, max_term,),
                get_min_valid_term(p, min_term, max_term),
            )
        )[:5]

        for p in filtered:
            print(p.kor_co_nm, p.fin_prdt_nm, get_max_rate_in_term(p, min_term, max_term))

        return Response(Serializer(filtered, many=True).data)

    except Exception as e:
        print('[ERROR]', e)
        print(format_exc())
        return Response({'error': '서버 내부 오류가 발생했습니다.'}, status=500)


def get_max_rate_in_term(product, min_term, max_term):
    valid_rates = []
    for opt in product.optionList.all():
        try:
            term = int(opt.save_trm)
            if min_term <= term <= max_term:
                valid_rates.append(opt.intr_rate)
        except (ValueError, TypeError):
            continue
    return max(valid_rates) if valid_rates else 0

def get_min_valid_term(product, min_term, max_term):
    terms = []
    for opt in product.optionList.all():
        try:
            term = int(opt.save_trm)
            if min_term <= term <= max_term:
                terms.append(term)
        except ValueError:
            continue
    return min(terms) if terms else 9999

def is_term_in_range(product, min_term, max_term):
    for opt in product.optionList.all():
        try:
            term = int(opt.save_trm)
            if min_term <= term <= max_term:
                return True
        except ValueError:
            continue
    return False

def is_age_eligible(join_member, user_age):
    numbers = list(map(int, re.findall(r'\d+', join_member or '')))
    if not numbers:
        return True
    elif len(numbers) == 1:
        return user_age >= numbers[0]
    elif len(numbers) >= 2:
        return numbers[0] <= user_age <= numbers[1]
    return True