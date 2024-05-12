from django.db import models

class Picture(models.Model):
    listing = models.ForeignKey('Listing', related_name='pictures', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listing_images/')


    def __str__(self):
        return f"Image for {self.listing.title} - {self.id}"

class Tag(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tags = models.ManyToManyField(Tag, related_name='listings')  # Fix: added related_name argument

    def __str__(self):
        return self.title
    
class Template(models.Model):
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=1200)
    category = models.TextField(choices=[
        (None, 'Wybierz kategorię'),
        ('bottom_garment', 'Bottom Garment'),
        ('top_garment', 'Top Garment'),
        ('accessories', 'Accessories')
    ])
    
    category = models.TextField(choices=[
        (None, 'Wybierz stan'),
        ('decent', 'Zadowalający'),
        ('good', 'Dobry'),
        ('very_good', 'Bardzo dobry'),
        ('new', 'Nowy bez metek'),
        ('new_with_tags', 'Nowy z metkami')
    ])
    size = models.TextField(choices=[
        (None, 'Wybierz rozmiar'),
        ('xxs', 'XXS'),
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TopGarment(models.Model):
    width = models.IntegerField()
    length = models.IntegerField()
    shoulder_width = models.IntegerField()
    sleeve_length = models.IntegerField()
    
class BottomGarment(models.Model):
    waist = models.IntegerField()
    hip = models.IntegerField()
    inseam = models.IntegerField()
    outseam = models.IntegerField()
    rise = models.IntegerField()
    