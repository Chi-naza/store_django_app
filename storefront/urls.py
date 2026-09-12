"""
URL configuration for storefront project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

admin.site.site_header = "Chinaza Dashboard"
admin.site.site_title = "Control Your E-commerce From Here"
admin.site.index_title = "Your E-commerce Platform"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path("store/", include("store.urls")),
    # docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

  
    # 🔑 AUTHENTICATION ENDPOINTS (Login, Logout, Password Reset, Password Change)
    path('api/auth/', include('dj_rest_auth.urls')),
    # 📝 REGISTRATION ENDPOINTS (Signup, Email Verification trigger)
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
