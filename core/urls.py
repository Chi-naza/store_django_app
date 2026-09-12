from django.urls import path, include
from django.views.generic import TemplateView
from dj_rest_auth.registration.views import  RegisterView, ResendEmailVerificationView
from . import views


registration_urlpatterns = [
    path('', RegisterView.as_view(), name='rest_register'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name='rest_resend_email'),
    path('verify-email/',  views.CustomVerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-email-verification-sent/', TemplateView.as_view(), name='account_email_verification_sent'),
]

urlpatterns = [
    path("", views.home),
    path("hello/", views.say_hello),
    # Registration Endpoints: (Signup, Email Verification trigger)
    path('api/auth/registration/', include(registration_urlpatterns)),
    # Auth Endpoints: (Login, Logout, Password Reset, Password Change)
    path('api/auth/', include('dj_rest_auth.urls')),
    # Social Login API Endpoints
    path('api/auth/google/', views.GoogleLoginView.as_view(), name='google_login'),
    path('api/auth/apple/', views.AppleLoginView.as_view(), name='apple_login'),
]