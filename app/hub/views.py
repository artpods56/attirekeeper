from django.shortcuts import render
from .models import Listing

def add(request):
    return render(request, "hub/add.html")

def gallery(request):
    items = Listing.objects.all()  # gets all objects from your model
    field_names = [field.name for field in Listing._meta.fields]
    return render(request, 'hub/gallery.html', {'items': items, 'field_names': field_names})

def settings(request):
    return render(request, 'hub/settings.html')


def panel(request):
    return render(request, 'hub/panel.html')