# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserInfoSerializer
from django.contrib.auth import get_user_model
from fin_products.models import TermDeposit, InstallmentSaving


User = get_user_model()

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserInfoSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mypage_view(request):
    # user = request.user  # 기존 코드
    # → prefetch_related로 optionList 포함시켜야 함
    user = (
        User.objects
        .prefetch_related(
            'joined_term_products__optionList',
            'joined_saving_products__optionList',
        )
        .get(pk=request.user.pk)
    )

    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('request.data:', request.data)  # 디버깅

        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            print('유효한 데이터:', serializer.validated_data)  # 디버깅

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 임의로 추가한 내 상품 데이터 함수
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sub_product(request):
    product_id = request.data.get('product_id')
    product_type = request.data.get('product_type')  # 'term' 또는 'saving'

    if not product_id or not product_type:
        return Response({"error": "product_id와 product_type이 필요합니다."}, status=400)

    user = request.user

    try:
        if product_type == 'term':
            product = TermDeposit.objects.get(fin_prdt_cd=product_id)
            user.joined_term_products.add(product)
        elif product_type == 'saving':
            product = InstallmentSaving.objects.get(fin_prdt_cd=product_id)
            user.joined_saving_products.add(product)
        else:
            return Response({"error": "올바르지 않은 product_type"}, status=400)
    except (TermDeposit.DoesNotExist, InstallmentSaving.DoesNotExist):
        return Response({"error": "상품을 찾을 수 없습니다."}, status=404)

    return Response({"message": "상품이 내 목록에 추가되었습니다."}, status=200)