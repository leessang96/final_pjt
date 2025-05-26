# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserInfoSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mypage_view(request):
    user = request.user

    if request.method == 'GET':
        serializer = UserInfoSerializer(user)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('request.data:', request.data)  # 들어온 데이터 확인

        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            print('유효한 데이터:', serializer.validated_data)  # 디버깅

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
