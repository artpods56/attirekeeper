from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.core.validators import validate_image_file_extension
import os

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    name = models.TextField()


    def __str__(self):
        return self.name
    
class Measurement(models.Model):
    measurements_id = models.AutoField(primary_key=True)
    width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    length = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    shoulder_width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    sleeve_length = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    waist = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    hip = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    inseam = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    


class Listing(models.Model):
        
    listing_id = models.AutoField(primary_key=True)
    title = models.CharField()
    description = models.TextField()
    
    default_size_choice = [(None, 'Not selected')]
    top_garment_sizes = [
        ('xxs', 'XXS'),
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL')]
    
    bottom_garment_sizes = [(f'us{x}', f'US {x}') for x in range(26,44)]
    
    size_choices = default_size_choice + top_garment_sizes + bottom_garment_sizes
    
    size_choices_map = {option[0]:'top_garment' for option in top_garment_sizes} | {option[0]:'bottom_garment' for option in bottom_garment_sizes}
    
    size = models.CharField(choices=size_choices, default=None)
    flaws = models.CharField(blank=True)
    brand = models.ForeignKey(Brand, null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    condition = models.CharField(choices=[
        (None, 'Not selected'),
        ('decent', 'Decent'),
        ('good', 'Good'),
        ('very_good', 'Very good'),
        ('new_without_tags', 'New without tags'),
        ('new_with_tags', 'New with tags')
    ], default=None)
    
    category = models.CharField(choices=[
        (None, 'Not selected'),
        ('bottom_garment', 'Bottom Garment'),
        ('top_garment', 'Top Garment'),
        ('accessories', 'Accessories')
    ], default=None)
    
    measurements_id = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title
    
    
    
class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='listing_photos/', null=True, blank=True, validators=[validate_image_file_extension])
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
     
    def __str__(self):
        return self.image.name

class Template(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.CharField()
    description = models.TextField(max_length=1200)
    
    def __str__(self):
        return self.name
    

@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)