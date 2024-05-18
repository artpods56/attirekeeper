from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os

class Measurements(models.Model):
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
    title = models.TextField()
    description = models.TextField()
    size = models.TextField(choices=[
        (None, 'Wybierz rozmiar'),
        ('XXS', 'XXS'),
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL')]
    )
    flaws = models.TextField(blank=True)
    brand = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    condition = models.TextField(choices=[
        (None, 'Wybierz stan'),
        ('decent', 'Zadowalający'),
        ('good', 'Dobry'),
        ('very_good', 'Bardzo dobry'),
        ('new', 'Nowy bez metek'),
        ('new_with_tags', 'Nowy z metkami')
    ], default=None)
    
    category = models.TextField(choices=[
        (None, 'Wybierz kategorię'),
        ('bottom_garment', 'Bottom Garment'),
        ('top_garment', 'Top Garment'),
        ('accessories', 'Accessories')
    ], default=None)
    
    measurements_id = models.ForeignKey(Measurements, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.title
    
    
    
class Photo(models.Model):
    photo_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='listing_photos/')
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    
    # def delete(self, *args, **kwargs):
    #     self.image.delete()
    #     super(Photo, self).delete(*args, **kwargs)
                       
                       
    def __str__(self):
        return self.image.name

class Template(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1200)
    
    def __str__(self):
        return self.name
    

@receiver(post_delete, sender=Photo)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)