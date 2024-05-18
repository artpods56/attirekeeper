from django.contrib import admin
from .models import *

admin.site.register(Listing)
admin.site.register(Template)
admin.site.register(Measurements)
admin.site.register(Photo)

