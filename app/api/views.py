from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.apps import apps
import logging
from hub.forms import TemplateForm
from hub.models import Template, Brand


logger = logging.getLogger( __name__ )
logger.setLevel(logging.DEBUG)
logger.info("Loaded logger")

def get_model_fields(request, model_name):

    excluded_types = ['AutoField', 'ForeignKey', 'OneToOneField', 'DateTimeField']
    model = apps.get_model('hub', model_name)

    model_fields = [field.name for field in model._meta.get_fields()
                    if field.get_internal_type() not in excluded_types]

    return JsonResponse(model_fields, safe=False)

def get_template(request, template_name):
    model = apps.get_model('hub', 'Template')
    try:
        template_objects = model.objects.values()
        result = template_objects.get(name=template_name)
        return JsonResponse(result, safe=False)
    except model.DoesNotExist:
        return JsonResponse({'error': 'Template not found'}, status=404)
   
def edit_template(request):
    logger.debug("Editing template.")
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            if Template.objects.filter(name=name).exists():
                Template.objects.filter(name=name).update(description=description)
                logger.info("Template updated.")
                return redirect('templates')
            else:
                logger.error("Template with this name does not exist.")
                form.add_error('name', 'Template with this name does not exist.')
                return redirect('templates')

def create_template(request):
    logger.debug("Creating new template.")
    if request.method == 'POST':
        form = TemplateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            if Template.objects.filter(name=name).exists():
                logger.error("Template with this name already exists.")
                form.add_error('name', 'Template with this name already exists.')
                return redirect('templates')
            else:
                logger.info("Template created.")
                form.save()
                return redirect('templates')
            
def create_listing(request):
    logger.debug("Creating new listing.")
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gallery')
        else:
            logger.error("Listing form is not valid.")
            return redirect('gallery')
    else:
        logger.error("Request is not POST.")
        return redirect('gallery')
    
def brand_autocomplete(request):
    if 'term' in request.GET:
        qs = Brand.objects.filter(name__icontains=request.GET.get('term'))
        names = list(qs.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)