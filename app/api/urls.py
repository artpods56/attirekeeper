from django.urls import path
from . import views

urlpatterns = [
    path('template/create/', views.create_template, name='create_template'),
    path('template/edit/', views.edit_template, name='edit_template'),
    path('<str:model_name>/fields/', views.get_model_fields, name='get_model_fields'),
    path('template/<str:template_name>/', views.get_template, name='get_template'),
    path('listings/', views.get_listings, name='get_listings'),
    path('listings/<int:listing_id>/', views.get_listings, name='get_listings'),
    path('listings/remove/', views.remove_listings, name='remove_listings'),
    path('measurements/', views.get_measurements, name='get_measurements'),
    path('measurements/<int:measurement_id>/', views.get_measurements, name='get_measurements'),
    path('purchases/', views.get_purchases, name='get_purchases'),
    path('purchases/<int:purchase_id>/', views.get_purchases, name='get_purchases'),
    
]