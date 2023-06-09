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
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('experienced', 'Experienced'),
        ('expert', 'Expert/Grandma')
    ]

    name = models.CharField(max_length = 48)
    category = models.CharField(max_length=64, choices=CATEGORIES)
    num_steps = models.IntegerField(default = 0)
    jarn_amount = models.FloatField(default = 0)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="recipes/", blank=False, default= '')
    difficulty = models.CharField(max_length=64, choices=DIFFICULTY)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")  
    favorites = models.ManyToManyField(User, blank=True, related_name="favorites")
    likes = models.ManyToManyField(User, blank=True, related_name="users_likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="user_dislikes")


    def __str__(self):
        return str(self.id) + '_' + str(self.name)
    
class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.IntegerField()
    description = models.TextField()
    bookmark_user = models.ManyToManyField(User, blank=True, related_name="bookmark_user")

    class Meta:
        unique_together = ['recipe', 'step']

    def __str__(self):
        return str(self.recipe) + '_step_' + str(self.step)
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                                    
    followed_users = models.ManyToManyField(User, blank=True, related_name="followed_users")

    def __str__(self):
        return str(self.user)

    

                     

