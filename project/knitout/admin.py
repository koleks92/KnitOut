from django.contrib import admin
from .models import User, Recipe

# Register your models here.
admin.site.register(User)
admin.site.register(Recipe)
