# Generated by Django 5.0.6 on 2024-06-08 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hub', '0004_alter_listing_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='size',
            field=models.CharField(choices=[(None, 'Not selected'), ('xxs', 'XXS'), ('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL'), ('xxxl', 'XXXL'), ('us26', 'US 26'), ('us27', 'US 27'), ('us28', 'US 28'), ('us29', 'US 29'), ('us30', 'US 30'), ('us31', 'US 31'), ('us32', 'US 32'), ('us33', 'US 33'), ('us34', 'US 34'), ('us35', 'US 35'), ('us36', 'US 36'), ('us37', 'US 37'), ('us38', 'US 38'), ('us39', 'US 39'), ('us40', 'US 40'), ('us41', 'US 41'), ('us42', 'US 42'), ('us43', 'US 43')], default=None),
        ),
    ]
