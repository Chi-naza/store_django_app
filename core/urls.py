from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path("", views.home),
    path("hello/", views.say_hello),
    path("users/", views.UsersListView.as_view()),
    # Simply POST a username/email and password here to automatically receive JWT tokens
    # path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/signup/', views.RegisterView.as_view(), name='auth_register'),
]