from django.urls import path
from . import views

urlpatterns = [
    path('<str:model_name>/fields/', views.get_model_fields, name='get_model_fields'),
]