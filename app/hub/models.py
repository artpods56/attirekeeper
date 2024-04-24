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