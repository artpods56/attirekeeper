# Generated by Django 5.0.6 on 2024-05-26 20:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('brand_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Measurements',
            fields=[
                ('measurements_id', models.AutoField(primary_key=True, serialize=False)),
                ('width', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('length', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('shoulder_width', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('sleeve_length', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('waist', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('hip', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('inseam', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=200)),
                ('description', models.TextField(max_length=1200)),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('listing_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('size', models.TextField(choices=[(None, 'Size'), ('XXS', 'XXS'), ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')])),
                ('flaws', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('condition', models.TextField(choices=[(None, 'Not selected'), ('decent', 'Decent'), ('good', 'Good'), ('very_good', 'Very good'), ('new_without_tags', 'New without tags'), ('new_with_tags', 'New with tags')], default=None)),
                ('category', models.TextField(choices=[(None, 'Not selected'), ('bottom_garment', 'Bottom Garment'), ('top_garment', 'Top Garment'), ('accessories', 'Accessories')], default=None)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hub.brands')),
                ('measurements_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.measurements')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='listing_photos/')),
                ('listing_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hub.listing')),
            ],
        ),
    ]
