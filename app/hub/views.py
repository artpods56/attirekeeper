from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from .models import Listing, Template, Measurement, Photo, Brand
from .forms import TemplateForm, ListingForm, PhotoForm, MeasurementsForm
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
import requests

import logging
import requests

logger = logging.getLogger( __name__ )
logger.setLevel(logging.DEBUG)
logger.info("Loaded views logger")

def add(request):
    return render(request, "hub/add.html")

def gallery(request):

    return render(request, 'hub/gallery.html')

def templates(request):
    logger.debug("Loading templates view.")
    listing_form = ListingForm()
    measurements_form = MeasurementsForm()
    photo_form = PhotoForm()
    return render(request, 'hub/pages/templates.html', {'listing_form': listing_form, 
                                              'measurements_form': measurements_form, 
                                              'photo_form': photo_form})
    
    
def items(request):
        listings = Listing.objects.prefetch_related('photo_set').all()

        # Prepare data for the template
        listing_data = []
        for listing in listings:
            photos = listing.photo_set.all()
            listing_data.append({
                'listing': listing,
                'photos': photos.first(),
            })

        # Pass the data to the template
        context = {
            'listing_data': listing_data,
        }

        return render(request, 'hub/pages/items.html', context)
    
def upload(request):
    logger.debug("View received a request")
    if request.method == 'POST':
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

            return redirect('upload')  # Replace with your success URL
    else:
        listing_form = ListingForm()
        measurements_form = MeasurementsForm()
        photo_form = PhotoForm()
    
    return render(request, 'hub/pages/upload.html', {
        'listing_form': listing_form,
        'measurements_form': measurements_form,
        'photo_form': photo_form
    })

def materials(request):
    return render(request, 'hub/materials.html')