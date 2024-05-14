from django.db import models

class Measurements(models.Model):
    measurements_id = models.AutoField(primary_key=True)
    width = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    shoulder_width = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    sleeve_length = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    hip = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    inseam = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    outseam = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    rise = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)


class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
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
    
class Template(models.Model):
    template_id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=200)
    description = models.TextField(max_length=1200)
    
    def __str__(self):
        return self.name
    
