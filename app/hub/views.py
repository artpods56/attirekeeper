from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .models import Listing, Template, TopGarment, BottomGarment
from .forms import TemplateForm

def add(request):
    return render(request, "hub/add.html")

def gallery(request):
    items = Listing.objects.all()  # gets all objects from your model
    field_names = [field.name for field in Listing._meta.fields]
    return render(request, 'hub/gallery.html', {'items': items, 'field_names': field_names})

def settings(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = TemplateForm()
    return render(request, 'hub/settings.html', {'form': form, 'templates' : Template.objects.all()})


def panel(request):
    return render(request, 'hub/panel.html')

def create_template(request):
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hub/settings.html')
    else:
        form = TemplateForm()
    return render(request, 'hub/settings.html', {'form': form, 'templates' : Template.objects.all()})

def get_fields(request, category):
    if category == 'top_garment':
        fields = [field.name for field in TopGarment._meta.get_fields()]
    elif category == 'bottom_garment':
        fields = [field.name for field in BottomGarment._meta.get_fields()]
    else:
        fields = []
    return JsonResponse(fields, safe=False)