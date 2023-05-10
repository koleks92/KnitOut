from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.contrib.auth.decorators import login_required

 
from .models import User, Recipe, Step

''' FORMS '''
class Recipe_Form(forms.Form):
    # Get categories and difficulties
    CATEGORIES = Recipe.CATEGORIES
    DIFFICULTY = Recipe.DIFFICULTY

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter name of the recipe'}))
    category = forms.ChoiceField(label="Category", widget=forms.Select, choices=CATEGORIES, initial=False)
    num_steps = forms.IntegerField(label="Number of Steps", widget=forms.NumberInput(attrs={'placeholder': 'Enter the number of steps'}))
    jarn_amount = forms.FloatField(label="Jarn Amount", widget=forms.NumberInput(attrs={'placeholder': 'Enter the amount of jarn needed'}))
    difficulty = forms.ChoiceField(label="Difficulty", widget=forms.Select, choices=DIFFICULTY, initial=False)

class Steps_Form(forms.Form):
    description = forms.CharField(label = "", widget=forms.Textarea(attrs={'placeholder': 'Enter step description'}))

''' VIEWS '''

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
            # Get recipie and check if valud
            recipe = Recipe_Form(request.POST)
            if recipe.is_valid():
                name = recipe.cleaned_data['name']
                category = recipe.cleaned_data['category']
                num_steps = recipe.cleaned_data['num_steps']  
                jarn_amount = recipe.cleaned_data['jarn_amount']   
                difficulty = recipe.cleaned_data['difficulty']
                user = request.user
                # Create Recipe instance and save
                recipe = Recipe(name = name,
                                category = category,
                                num_steps = num_steps,
                                jarn_amount = jarn_amount,
                                difficulty = difficulty,
                                user = user)
                recipe.save() 

                # Redirect to add_steps
                return redirect('add_steps', id=recipe.id)

        else:
            # Render form in not POST
            return render(request, "knitout/add_recipe.html",{
                "add_form": Recipe_Form()
            })
    except:
        return render(request, "knitout/error.html",{
            "message": "Something went wrong! Please try again."
        })
        
@login_required
def add_steps(request, id):
    # Get recipe and number of steps to add
    recipe = get_object_or_404(Recipe, id = id)
    num_steps = recipe.num_steps

    # Create formset_factory for Steps_Form
    Steps_FormsSet = forms.formset_factory(Steps_Form, extra = num_steps)

    if request.method == "POST":
        form_steps = Steps_FormsSet(request.POST)
        if form_steps.is_valid():
            # Get steps with descriptions
            for step, description in enumerate(form_steps, start=1):
                # Get clean description
                description = description.cleaned_data['description']
                step = Step(recipe = recipe,
                            step = step,
                            description = description)
                step.save()
            
            return render(request, "knitout/index.html", {
                "message": "Recipie added successfully"
            })

    else:
        # Create FormsSet 
        form_steps = Steps_FormsSet()

        return render(request, "knitout/add_steps.html",{
            "form_steps": form_steps
        })
    


