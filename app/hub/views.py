from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from .models import Listing, Template, Measurements
from .forms import TemplateForm
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError

import logging

logger = logging.getLogger( __name__ )
logger.setLevel(logging.DEBUG)
logger.info("Loaded logger")

def add(request):
    return render(request, "hub/add.html")

def gallery(request):
    items = Listing.objects.all()  # gets all objects from your model
    field_names = [field.name for field in Listing._meta.fields]
    return render(request, 'hub/gallery.html', {'items': items, 'field_names': field_names})

def settings(request):
    logger.debug("Loading settings view.")
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Template.objects.filter(name=name).exists():
                logger.error("Template with this name already exists.")
                form.add_error('name', 'Template with this name already exists.')
            else:
                logger.info("Template created.")
                form.save()
                return redirect('settings')
    else:
        form = TemplateForm()
    return render(request, 'hub/settings.html', {'form': form, 'templates' : Template.objects.all()})


def panel(request):
    logger.debug("Loading panel view.")
    return render(request, 'hub/panel.html')



def get_fields(request):
    # if not request.is_ajax():
    #     raise Http404
    
    excluded_types = ['AutoField', 'ForeignKey', 'OneToOneField']
    
    listing_fields = [field.name for field in Listing._meta.get_fields() 
                      if field.get_internal_type() not in excluded_types]
    
    measurements_fields = [field.name for field in Measurements._meta.get_fields() 
                           if field.get_internal_type() not in excluded_types]
    
    return JsonResponse(listing_fields + measurements_fields, safe=False)

def get_template(request, template_name):
    if template_name == "":
        raise Http404
    else:
        template = Template.objects.get(name=template_name)
        return JsonResponse({'name': template.name, 'description': template.description})