from django.contrib import admin
from .models import User, Recipe, Step, Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Recipe)
admin.site.register(Step)
admin.site.register(Follow)
