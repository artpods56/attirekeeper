from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.apps import apps
import logging
from hub.forms import TemplateForm
from django.forms.models import model_to_dict
from hub.models import Template, Brand, Listing, Purchase


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


def get_listings(request, listing_id=None):
    if listing_id:
        listings = Listing.objects.prefetch_related('photo_set').filter(listing_id=listing_id)
    else:
        listings = Listing.objects.prefetch_related('photo_set').all()
    
    # Prepare data for JSON serialization
    listing_data = []
    for listing in listings:
        listing_dict = model_to_dict(listing)
        
        # Handle ImageFields
        for field_name, value in listing_dict.items():
            if hasattr(value, 'url'):
                listing_dict[field_name] = request.build_absolute_uri(value.url)
        
        photos = listing.photo_set.all()
        listing_dict['photos'] = [{
            'id': photo.photo_id,
            'url': request.build_absolute_uri(photo.image.url) if photo.image else None,
            # Add other photo fields as needed
        } for photo in photos]
        
        listing_data.append(listing_dict)
    
    return JsonResponse({'rows': listing_data, 'total': listings.count()})


def get_purchases(request, purchase_id=None):
    if purchase_id:
        purchases = Purchase.objects.select_related().filter(purchase_id=purchase_id)
    else:
        purchases = Purchase.objects.select_related().all()
    
    purchase_data = []
    for purchase in purchases:
        purchase_dict = model_to_dict(purchase)
        purchase_data.append(purchase_dict)
    
    return JsonResponse({'rows': purchase_data, 'total': purchases.count()})
                        
                        
                        
def remove_listings(request):
    ids = request.POST.getlist('listing_ids[]')
    response = Listing.objects.filter(listing_id=ids).delete()
    if response[0] == 0:
        return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'success'})