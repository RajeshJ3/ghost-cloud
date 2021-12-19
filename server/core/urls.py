from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import permissions
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Ghost Cloud API Docs",
      default_version='v1',
      description="API documentation for Ghost Cloud",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="joshirajesh448@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('objects/', include('objects.urls')),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    from django.conf.urls.static import  static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
