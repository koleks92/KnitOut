from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User, Recipe

''' FORMS '''
class Recipe_Form(forms.Form):
    # Get categories and difficulties
    CATEGORIES = Recipe.CATEGORIES
    DIFFICULTY = Recipe.DIFFICULTY

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter name of the recipe'}))
    category = forms.ChoiceField(label="Category", widget=forms.Select, choices=CATEGORIES, initial=False)
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder': 'Enter the recipe'}))
    difficulty = forms.ChoiceField(label="Difficulty", widget=forms.Select, choices=DIFFICULTY, initial=False)


# Create your views here.

def index(request):
    return render(request, "knitout/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "knitout/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "knitout/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "knitout/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "knitout/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
    else:
        return render(request, "knitout/register.html")
    
@login_required
def add_recipe(request):
    try:
        if request.method == "POST":
            recipe = Recipe_Form(request.POST)
            if recipe.is_valid():
                name = recipe.cleaned_data['name']
                category = recipe.cleaned_data['category']
                description = recipe.cleaned_data['description']     
                difficulty = recipe.cleaned_data['difficulty']
                user = request.user

                recipe = Recipe(name = name, category = category, description = description, difficulty = difficulty, user = user)
                recipe.save() 

            return render(request, "knitout/index.html",{
                "message": "New Recipe Added!"
            })
        else:
            return render(request, "knitout/add_recipe.html",{
                "add_form": Recipe_Form()
            })
    except:
        return render(request, "knitout/error.html",{
            "message": "Something went wrong! Please try again."
        })