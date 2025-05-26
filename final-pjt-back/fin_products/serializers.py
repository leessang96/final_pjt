
from rest_framework import serializers
from .models import (
    TermDeposit, TermDepositOption,
    InstallmentSaving, InstallmentSavingOption
)

# 예금
class TermDepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermDepositOption
        fields = ['save_trm', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2']

class TermDepositSerializer(serializers.ModelSerializer):
    optionList = TermDepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = TermDeposit
        fields = '__all__'


# 적금
class InstallmentSavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentSavingOption
        fields = ['save_trm', 'intr_rate_type_nm', 'intr_rate', 'intr_rate2']

class InstallmentSavingSerializer(serializers.ModelSerializer):
    optionList = InstallmentSavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = InstallmentSaving
        fields = '__all__'
