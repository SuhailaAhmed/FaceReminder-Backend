"""Gp_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from django.conf.urls.static import static
from Gp_Backend import settings
from django.contrib import admin



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

schema_view = get_schema_view(
   openapi.Info(
        title="GP Backend APIs",
        default_version='GP Backend APIs v1',
        description="GP Backend APIs",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns += [
   path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)