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
from django.conf import settings
from django.conf.urls.static import static
from hub.views import items_router, templates, items, purchases

urlpatterns = [
    path('admin/', admin.site.urls),
    path('templates/', templates, name='templates'),
    path('templates/<str:tas>/<int:id>/', templates, name='templates'),
    path('items/', items, name='items'),
    path('items/<str:task>/', items_router, name='items_router'),
    path('items/<str:task>/<int:id>/', items_router, name='items_router'),
    path('purchases/', purchases, name='purchases'),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

