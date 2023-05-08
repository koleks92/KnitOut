from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass

class Recipe(models.Model):
    CATEGORIES = [
        ('', 'Choose Category'),
        ('hats', "Hats"),
        ('sweaters', 'Sweaters and Jumpers'),
        ('scarves', 'Scarves'),
        ('blankets', 'Blankets and Throws'),
        ('cardigans', 'Cardigans'),
        ('socks', 'Socks'),
        ('gloves', 'Gloves'),
        ('toys', 'Toys'),
        ('other', 'Other')
    ]

    DIFFICULTY = [
        ('', 'Choose level'),
        ('begginer', 'Begginer'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
        ('expert', 'Expert/Grandma')
    ]

    name = models.CharField(max_length = 48)
    category = models.CharField(max_length=64, choices=CATEGORIES)
    description = models.CharField(max_length=6400)
    date = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=64, choices=DIFFICULTY)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")  
    favorite = models.ManyToManyField(User, blank=True, related_name="favorites")

    def __str__(self):
        return str(self.id) + '_' + str(self.name)
                     

