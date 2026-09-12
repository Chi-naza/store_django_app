from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer, VerifyEmailSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import SetPasswordForm
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from .adapters import EMAIL_OTP_CACHE_PREFIX


UserModel = get_user_model()

OTP_CACHE_PREFIX = "password_reset_otp_"
OTP_TIMEOUT = 60 * 10  # 10 minutes



# Custom Registration Fields mapping directly to Extended User Model
class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    phone_number = serializers.CharField(required=True, max_length=20)
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_email(self, email):
        email = super().validate_email(email)
        if UserModel.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address."
            )
        return email

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user


# Custom OTP Verification for Registration
class CustomVerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)

    def validate(self, attrs):
        cache_key = f"{EMAIL_OTP_CACHE_PREFIX}{attrs['otp']}"
        user_pk = cache.get(cache_key)

        if not user_pk:
            raise serializers.ValidationError({"otp": "Invalid or expired code."})

        try:
            user = UserModel.objects.get(pk=user_pk)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid or expired code."})

        self.user = user
        self.cache_key = cache_key
        return attrs

    def save(self, request):
        email_address, _created = EmailAddress.objects.get_or_create(
            user=self.user, email=self.user.email,
        )
        if not email_address.verified:
            get_adapter(request).confirm_email(request, email_address)
        cache.delete(self.cache_key)
        return email_address


class CustomLoginSerializer(LoginSerializer):
    # Completely remove the default username field mapping definition
    username = None
    
    # 📧 Explicitly declare email and password as your only payload properties
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    token = None  # remove the inherited field
    otp = serializers.CharField(required=True, source="token")

    def validate(self, attrs):
        return super().validate(attrs)
    


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        return value

    def save(self):
        email = self.validated_data['email']
        try:
            user = UserModel.objects.get(email__iexact=email, is_active=True)
        except UserModel.DoesNotExist:
            return  # fail silently — don't reveal whether the email exists

        # Generate an OTP that isn't already active for someone else
        for _ in range(5):
            otp = get_random_string(6, allowed_chars='0123456789')
            cache_key = f"{OTP_CACHE_PREFIX}{otp}"
            if cache.add(cache_key, user.pk, timeout=OTP_TIMEOUT):
                break
        else:
            raise Exception("Could not generate a unique OTP, try again.")

        send_mail(
            subject="Your password reset code",
            message=f"Your password reset code is {otp}. It expires in 10 minutes.",
            from_email=None,
            recipient_list=[user.email],
        )


class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    uid = None
    token = None
    otp = serializers.CharField(required=True, source="token")

    def validate(self, attrs):
        otp = attrs.get('token')
        cache_key = f"{OTP_CACHE_PREFIX}{otp}"
        user_pk = cache.get(cache_key)

        if not user_pk:
            raise serializers.ValidationError({"otp": "Invalid or expired code."})

        try:
            user = UserModel.objects.get(pk=user_pk, is_active=True)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({"otp": "Invalid or expired code."})

        self.set_password_form = SetPasswordForm(user=user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        self.user = user
        self.cache_key = cache_key
        return attrs

    def save(self):
        self.set_password_form.save()
        cache.delete(self.cache_key)