from django.test import TestCase
from .models import Measurements, Listing, Photo, Template
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class TestModels(TestCase):
    def test_template_creation(self):
        template = Template.objects.create(
            name="Test Template",
            description="This is a test template",
        )
        self.assertIsNotNone(template)
        
    def test_listing_creation(self):
        measurements = Measurements.objects.create(
            width=10.5,
            length=20.5,
            shoulder_width=15.5,
            sleeve_length=25.5,
            waist=30.5,
            hip=35.5,
            inseam=40.5,
        )
        
        listing = Listing.objects.create(
            title="Test Listing",
            description="This is a test listing",
            size="M",
            flaws="None",
            brand="Test Brand",
            price=19.99,
            condition="good",
            category="top_garment",
            measurements_id=measurements,
        )
        photo = Photo.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
        )
        self.assertIsNotNone(photo)
        self.assertIsNotNone(listing)
        listing.delete()

    def test_foreign_key_binding(self):
        measurements = Measurements.objects.create(
            width=10.5,
            length=20.5,
            shoulder_width=15.5,
            sleeve_length=25.5,
            waist=30.5,
            hip=35.5,
            inseam=40.5,
        )
        
        listing = Listing.objects.create(
            title="Test Listing",
            description="This is a test listing",
            size="M",
            flaws="None",
            brand="Test Brand",
            price=19.99,
            condition="good",
            category="top_garment",
            measurements_id=measurements,
        )
        
        photo = Photo.objects.create(
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
        )
        
        self.assertEqual(listing.measurements_id, measurements) # Check if measurements_id is bound to listing
        self.assertEqual(photo.listing_id, listing) # Check if listing_id is bound to photo
        
        listing.delete()
        
    def test_cascade_delete(self):
        measurements = Measurements.objects.create(
            width=10.5,
            length=20.5,
            shoulder_width=15.5,
            sleeve_length=25.5,
            waist=30.5,
            hip=35.5,
            inseam=40.5,
        )
        
        listing = Listing.objects.create(
            title="Test Listing",
            description="This is a test listing",
            size="M",
            flaws="None",
            brand="Test Brand",
            price=19.99,
            condition="good",
            category="top_garment",
            measurements_id=measurements,
        )
        
        
        photo = Photo.objects.create(
            # image= 'test_image.jpg',
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
        )
        
        

        image_path = photo.image.path
        listing.delete() # Delete listing
        self.assertFalse(Photo.objects.filter(pk=photo.pk).exists()) # Check if photo was deleted
        print('Photo deleted')
        self.assertTrue(Measurements.objects.filter(pk=measurements.pk).exists())  # Measurements should still exist because they are not dependent on listing
        self.assertFalse(os.path.exists(image_path)) # Check if image file was deleted
        