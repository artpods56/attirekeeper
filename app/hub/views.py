from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, Http404
from .models import Listing, Template, Measurements
from .forms import TemplateForm, ListingForm, PhotoForm, MeasurementsForm
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
import requests

import logging
import requests

logger = logging.getLogger( __name__ )
logger.setLevel(logging.DEBUG)
logger.info("Loaded logger")

def add(request):
    return render(request, "hub/add.html")

def gallery(request):

    return render(request, 'hub/gallery.html')

def templates(request):
    logger.debug("Loading templates view.")
    form = TemplateForm()
    return render(request, 'hub/templates.html', {'form': form, 'templates' : Template.objects.all()})

def panel(request):
    logger.debug("Loading panel view.")
    listing_form = ListingForm()
    measurements_form = MeasurementsForm()
    
    
    photo_form = PhotoForm()
    return render(request, 'hub/panel.html', {'listing_form': listing_form, 
                                              'measurements_form': measurements_form, 
                                              'photo_form': photo_form})

def upload_file(request):
    if request.method == 'POST':
        listing_form = ListingForm(request.POST)
        measurements_form = MeasurementsForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        
        if listing_form.is_valid() and measurements_form.is_valid() and photo_form.is_valid():
            # Save the Measurements instance first
            measurements_instance = measurements_form.save()

            # Then save the Listing instance, attaching the Measurements instance
            listing_instance = listing_form.save(commit=False)
            listing_instance.measurements_id = measurements_instance
            
            listing_instance.save()
            
            # Finally, save the Photo instance, attaching the Listing instance
            files = request.FILES.getlist('image')
            logger.debug(files)
            for f in files:
                photo_instance = photo_form.save(commit=False)
                photo_instance.listing_id = listing_instance
                photo_instance.image = f
                photo_instance.save()

            
            return redirect('upload_file')
    else:
        listing_form = ListingForm()
        measurements_form = MeasurementsForm()
        photo_form = PhotoForm()
        
    return render(request, 'hub/upload.html', {
        'listing_form': listing_form, 
        'measurements_form': measurements_form, 
        'photo_form': photo_form
    })