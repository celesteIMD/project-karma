from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Building)
admin.site.register(Room)
admin.site.register(Review)
admin.site.register(Photo)
admin.site.register(Tag)
admin.site.register(Profile)