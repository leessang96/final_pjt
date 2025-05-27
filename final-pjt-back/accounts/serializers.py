from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from fin_products.models import TermDeposit, InstallmentSaving
from fin_products.serializers import TermDepositSerializer, InstallmentSavingSerializer


class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    salary = serializers.IntegerField(required=False, allow_null=True)
    current_amount = serializers.IntegerField(required=False, allow_null=True)
    email = serializers.EmailField(required=True)
    sub_product = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickname'] = self.validated_data.get('nickname', '')
        data['age'] = self.validated_data.get('age', '')
        data['salary'] = self.validated_data.get('salary', None)
        data['current_amount'] = self.validated_data.get('current_amount', None)
        data['username'] = self.validated_data.get('username', '')
        data['email'] = self.validated_data.get('email', '')
        data['sub_product'] = self.validated_data.get('sub_product', '')
        data['profile_image'] = self.validated_data.get('profile_image', None)
        return data

    def save(self, request):
        user = super().save(request)
        user.nickname = self.validated_data.get('nickname', '')
        user.age = self.validated_data.get('age', '')
        user.salary = self.validated_data.get('salary', None)
        user.current_amount = self.validated_data.get('current_amount', None)
        user.username = self.validated_data.get('username', '')
        user.email = self.validated_data.get('email', '')
        user.sub_product = self.validated_data.get('sub_product', '')
        user.profile_image = self.validated_data.get('profile_image', None)
        user.save()
        return user


class SimpleTermDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDeposit
        fields = ['fin_prdt_cd', 'fin_prdt_nm']  # 필요한 필드만 선택


class SimpleInstallmentSavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSaving
        fields = ['fin_prdt_cd', 'fin_prdt_nm']  # 필요한 필드만 선택


class UserInfoSerializer(serializers.ModelSerializer):
    
    joined_term_products = TermDepositSerializer(many=True, read_only=True)
    joined_saving_products = InstallmentSavingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',  # 회원 번호
            'username',  # ID
            'nickname',
            'email',
            'age',
            'salary',
            'current_amount',
            'profile_image',
            'joined_term_products',
            'joined_saving_products',
        ]
        read_only_fields = ['id', 'username']

