from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    sub_product = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['age'] = self.validated_data.get('age', '')
        data['username'] = self.validated_data.get('username', '')
        data['email'] = self.validated_data.get('email', '')
        data['sub_product'] = self.validated_data.get('sub_product', '')
        data['profile_image'] = self.validated_data.get('profile_image', None)
        return data
    

    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age', '')
        user.username = self.validated_data.get('username', '')
        user.email = self.validated_data.get('email', '')
        user.sub_product = self.validated_data.get('sub_product', '')
        user.profile_image = self.validated_data.get('profile_image', None)
        user.save()
        return user