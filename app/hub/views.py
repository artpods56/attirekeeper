from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Listing, Template, Measurement, Photo, Brand, Purchase
from .forms import TemplateForm, ListingForm, PhotoForm, MeasurementsForm, PurchaseForm
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
from django.forms import modelformset_factory
import json
from io import BytesIO
from PIL import Image

import logging
import requests
from django.core import serializers

logger = logging.getLogger( __name__ )
logger.setLevel(logging.DEBUG)
logger.info("Loaded views logger")


def model_to_dict(instance):
    serialized = serializers.serialize('json', [instance])
    data = json.loads(serialized)[0]['fields']
    
    data = {key: value if value is not None else '-' for key, value in data.items() if '_at' not in key}
    
    logger.debug(f"Model to dict: {data}")
    
    
    return data

def add(request):
    return render(request, "hub/add.html")

def gallery(request):

    return render(request, 'hub/gallery.html')

def templates(request, task = None, id = None):
    
    listings = Listing.objects.all()
    templates = Template.objects.all()
    measurements = Measurement.objects.all()
    listing_fields = [field.name for field in Listing._meta.get_fields()]
    measurements_fields = [field.name for field in Measurement._meta.get_fields()]
    logger.debug(f"Listing fields: {listing_fields+measurements_fields}")


    if request.method == 'POST':
        template_form = TemplateForm(request.POST)
        if template_form.is_valid():
            template_form.save()
            return redirect('templates')

    else:
        template_form = TemplateForm()
    
    listing_data = {}
    
    for listing in listings:
        listing_id = listing.__dict__['measurements_id_id']
        measurement = get_object_or_404(Measurement, pk=listing_id)
        
        listing_data[listing.__dict__['title']] = json.dumps({**model_to_dict(listing),**model_to_dict(measurement)})
    
    context = {
        'template_form': template_form,
        'listings': listings,
        'model_fields': filter(lambda x: '_id' not in x, set(listing_fields+measurements_fields)),
        'current_template_id' : id,
        'templates_data': templates,
        'listings_data': listing_data
    }
    
    if task == 'view' and id:
        template = get_object_or_404(Template, pk=id)
        template_form = TemplateForm(initial=template.__dict__)
        context['template_form'] = template_form
        

    
    return render(request, 'hub/pages/templates.html', context=context)
    
    
def items(request):
    return render(request, 'hub/pages/items.html')
    
def items_router(request, task = None, id = None):
    
    if task == 'view' and id:
        return items_view(request, id)
    if task == 'update' and id:
        return items_update(request, id)
    
    logger.debug("View received a request")
    if request.method == 'POST':
        
        if task == 'create':
            logger.debug("Got a POST request")
            listing_form = ListingForm(request.POST)
            measurements_form = MeasurementsForm(request.POST)
            photo_form = PhotoForm(request.POST, request.FILES)

            for form in [listing_form, measurements_form]:
                if form.is_valid():
                    for key, value in form.cleaned_data.items():
                        logger.debug(f"{key}: {value}")
                else:
                    logger.debug(f"{form} is not valid")
                    
            logger.debug(f"FILES data: {request.FILES}")

            if listing_form.is_valid() and measurements_form.is_valid():
                listing = listing_form.save(commit=False)
                measurements = measurements_form.save()
                listing.measurements_id = measurements
                listing.save()

                for file in request.FILES.getlist('image'):
                    photo = Photo(listing_id=listing, image=file)
                    photo.save()

                return redirect('items')  # Replace with your success URL

   
    listing_form = ListingForm()
    measurements_form = MeasurementsForm()
    photo_form = PhotoForm()

    
    context = {
        'task': task,
        'listing_form': listing_form,
        'measurements_form': measurements_form,
        'photo_form': photo_form
    }
    
    
    
    return render(request, 'hub/pages/upload.html', context=context)

def items_view(request, id):
    listing = get_object_or_404(Listing, pk=id)
    
    
    measurement_id = listing.__dict__['measurements_id_id']
    measurements = get_object_or_404(Measurement, pk=measurement_id)
    
    listing_form = ListingForm(initial=listing.__dict__)
    measurements_form = MeasurementsForm(initial=listing.measurements_id.__dict__)
    photo_form = PhotoForm()
    
    photos = listing.photo_set.all()
    templates = Template.objects.all()
    
  
    listings = Listing.objects.all()
  
    listing_data = model_to_dict(listing)
    measurements_data = model_to_dict(measurements)
  
    item_data = {**listing_data, **measurements_data}
    item_data_json = json.dumps(item_data)
  
    # If you want to pass the photo data (e.g., id, url) to the context for display purposes
    photos = {
        "photos": [{
            "id": photo.photo_id,
            "url": request.build_absolute_uri(photo.image.url) if photo.image else None,
            # Add other photo fields as needed
        } for photo in photos],
    }

    context = {
        'id': id,
        'listing_form': listing_form,
        'measurements_form': measurements_form,
        'photo_form': photo_form,
        'templates': templates,
        'listings': listings,
        'item_data': item_data_json,
        'photos_data': json.dumps(photos['photos'])
    }

    return render(request, 'hub/pages/upload.html', context=context)

def items_update(request, id):
    logger.debug("View received an update request")
    
    listing = get_object_or_404(Listing, pk=id)
    listing_form = ListingForm(request.POST or None, instance=listing)
    measurements_form = MeasurementsForm(request.POST or None, instance=listing.measurements_id)
    photo_form = PhotoForm(request.POST or None, request.FILES or None)


    if listing_form.is_valid() and measurements_form.is_valid() and photo_form.is_valid():
        
        # remove old photos
        listing.photo_set.all().delete()
        
        logger.debug("Forms are valid")
        listing = listing_form.save(commit=False)
        measurements = measurements_form.save()
        listing.measurements_id = measurements
        listing.save()

        for file in request.FILES.getlist('image'):
            photo = Photo(listing_id=listing, image=file)
            photo.save()

        return redirect('items')  # Replace with your success URL



def materials(request):
    return render(request, 'hub/materials.html')


def purchases(request):
    if request.method == 'POST':
        purchase_form = PurchaseForm(request.POST)
        if purchase_form.is_valid():
            purchase_form.save()
            return redirect('purchases')

    purchase_form = PurchaseForm()
    listing_form = ListingForm()
    return render(request, 'hub/pages/purchases.html', {'purchase_form': purchase_form,
                                                        'listing_form': listing_form})