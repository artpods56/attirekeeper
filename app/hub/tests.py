from django.test import TestCase, Client
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from django.urls import reverse
from .models import Measurements, Listing, Photo, Template
from .forms import ListingForm, MeasurementsForm, PhotoForm
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
        
        
    def test_listing_multiple_photos(self):
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
        photo_1 = Photo.objects.create(
            image=SimpleUploadedFile("test_image1.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
        )
        photo_2 = Photo.objects.create(
            image = SimpleUploadedFile("test_image2.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
            )
        
        assert len(listing.photo_set.all()) == 2
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
        
        
        photo_1 = Photo.objects.create(
            image=SimpleUploadedFile("test_image1.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
        )
        photo_2 = Photo.objects.create(
            image = SimpleUploadedFile("test_image2.jpg", b"file_content", content_type="image/jpeg"),
            listing_id=listing,
            )
        
        
        photo_1_path = photo_1.image.path
        photo_2_path = photo_2.image.path

        listing.delete() # Delete listing
        
        self.assertFalse(Photo.objects.filter(pk=photo_1.pk).exists()) # Check if first photo was deleted
        self.assertFalse(Photo.objects.filter(pk=photo_2.pk).exists()) # Check if second photo was deleted
        print('Photos were deleted')
        
        self.assertTrue(Measurements.objects.filter(pk=measurements.pk).exists())  # Measurements should still exist because they are not dependent on listing
        
        self.assertFalse(os.path.exists(photo_1_path)) # Check if first image file was deleted
        self.assertFalse(os.path.exists(photo_2_path)) # Check if second image file was deleted
        

class UploadFileViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_listing_with_multiple_images(self):
        # Create test images
        image1 = SimpleUploadedFile("image1.jpg", b"file_content", content_type="image/jpeg")
        image2 = SimpleUploadedFile("image2.jpg", b"file_content", content_type="image/jpeg")
        image3 = SimpleUploadedFile("image3.jpg", b"file_content", content_type="image/jpeg")

        # Create test data
        listing_data = {
            'title': 'Test Listing',
            'description': 'Test description',
            'size': 'M',
            'flaws': 'No flaws',
            'brand': 'Test brand',
            'price': 10.99,
            'condition': 'good',
            'category': 'top_garment',
            'width': 10.5,
            'length': 20.5,
            'shoulder_width': 15.5,
            'sleeve_length': 25.5,
            'waist': 30.5,
            'hip': 35.5,
            'inseam': 40.5,
            'image': [image1, image2, image3]
        }
        
        data = {f'id_{x}': y for x, y in listing_data.items()}
        # Create test request

        print(data)
        url = reverse('upload_file')
        


        response = self.client.post(url,
                                    data = data,
                                    content_type=MULTIPART_CONTENT,
                                    HTTP_AUTHORIZATION='Token {self.token.key}')

        # Check that the listing was created
        self.assertEqual(response.status_code, 200)  # Redirect to success page
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(Measurements.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 3)

        # Check that the images were uploaded
        listing = Listing.objects.get(title='Test Listing')
        photos = Photo.objects.filter(listing_id=listing)
        self.assertEqual(photos.count(), 3)
        for photo in photos:
            self.assertTrue(photo.image.name.endswith(('.jpg', '.jpeg')))