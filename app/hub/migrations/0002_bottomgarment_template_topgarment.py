# Generated by Django 3.2.13 on 2024-05-12 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BottomGarment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waist', models.IntegerField()),
                ('hip', models.IntegerField()),
                ('inseam', models.IntegerField()),
                ('outseam', models.IntegerField()),
                ('rise', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=1200)),
                ('category', models.TextField(choices=[(None, 'Wybierz kategorię'), ('bottom_garment', 'Bottom Garment'), ('top_garment', 'Top Garment'), ('accessories', 'Accessories')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopGarment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.IntegerField()),
                ('length', models.IntegerField()),
                ('shoulder_width', models.IntegerField()),
                ('sleeve_length', models.IntegerField()),
            ],
        ),
    ]
