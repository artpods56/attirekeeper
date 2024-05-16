"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from hub.views import gallery, add, settings, panel, get_fields, get_template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gallery/', gallery, name='gallery'),
    path('add/', add, name='add'),
    path('settings/', settings, name='settings'),
    path('panel/', panel, name='panel'),
    path('get_fields/', get_fields, name='get_fields'),
    path('get_template/<str:template_name>/', get_template, name='create_template'),
    path('api/', include('api.urls')),
]