from rest_framework import serializers
from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email", "first_name", "last_name", "phone_number", "bio", "profile_picture"]


class RegisterSerializer(serializers.ModelSerializer):
    
    # Ensure email is unique and password has a minimum length
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, min_length=8
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "username", "first_name", "last_name"]

    def create(self, validated_data):
        # Use create_user to automatically handle password hashing safely
        user = get_user_model().objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user



# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # 1. Let the parent class handle authentication and token generation
#         data = super().validate(attrs)
        
#         # 2. Inject your custom keys into the final server response dict
#         data['username'] = self.user.username
#         data['email'] = self.user.email
#         data['is_staff'] = self.user.is_staff
        
#         return data