from allauth.account.adapter import DefaultAccountAdapter
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.core.mail import send_mail

EMAIL_OTP_CACHE_PREFIX = "email_verify_otp_"
EMAIL_OTP_TIMEOUT = 60 * 10  # 10 minutes


class OTPAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        user = emailconfirmation.email_address.user

        for _ in range(5):
            otp = get_random_string(6, allowed_chars='0123456789')
            cache_key = f"{EMAIL_OTP_CACHE_PREFIX}{otp}"
            if cache.add(cache_key, user.pk, timeout=EMAIL_OTP_TIMEOUT):
                break
        else:
            raise Exception("Could not generate a unique OTP, try again.")

        send_mail(
            subject="Please Confirm Your Email Address",
            message=f"Thank you for registering. Your verification code is: {otp}",
            from_email=None,
            recipient_list=[emailconfirmation.email_address.email],
        )
