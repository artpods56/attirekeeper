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
from hub.views import gallery, add, templates, panel, upload_file, materials

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gallery/', gallery, name='gallery'),
    path('templates/', templates, name='templates'),
    path('panel/', panel, name='panel'),
    path('upload/', upload_file, name='upload_file'),
    path('api/', include('api.urls')),
    path('materials/', materials, name='materials'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)