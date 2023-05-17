from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

 
from .models import User, Recipe, Step, Follow

''' FORMS '''
class Recipe_Form(forms.Form):
    # Get categories and difficulties
    CATEGORIES = Recipe.CATEGORIES
    DIFFICULTY = Recipe.DIFFICULTY

    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter name of the recipe'}))
    category = forms.ChoiceField(label="Category", widget=forms.Select, choices=CATEGORIES, initial=False)
    num_steps = forms.IntegerField(label="Number of Steps", min_value=2, widget=forms.NumberInput(attrs={'placeholder': 'Enter the number of steps'}))
    jarn_amount = forms.FloatField(label="Jarn Amount", min_value=0.1, widget=forms.NumberInput(attrs={'placeholder': 'Enter the amount of jarn needed'}))
    difficulty = forms.ChoiceField(label="Difficulty", widget=forms.Select, choices=DIFFICULTY, initial=False)

class Steps_Form(forms.Form):
    description = forms.CharField(label = "", required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter step description'}))

''' VIEWS '''

def index(request):
    recipes_follow = False

    # Get 2 recent favorites
    if request.user.is_authenticated:
        recipes_follow = Recipe.objects.filter(favorites = request.user).order_by('-date')[:2]
         
    # Get 10 recent recipes
    recipes_all = Recipe.objects.order_by('-date')[:10]


    return render(request, "knitout/index.html", {
        "recipes_follow": recipes_follow,
        "recipes_all": recipes_all
    })


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
    try:
        # Get recipe and number of steps to add
        recipe = get_object_or_404(Recipe, id = id)
        num_steps = recipe.num_steps

        # Create formset_factory for Steps_Form
        Steps_FormsSet = forms.formset_factory(Steps_Form, extra = num_steps)

        if request.method == "POST":
            form_steps = Steps_FormsSet(request.POST)
            if form_steps.is_valid():
                # Get steps with descriptions
                for step, description in enumerate(form_steps, start=0):
                    # Get clean description
                    description = description.cleaned_data['description']
                    step_recipe = Step(recipe = recipe,
                                step = step,
                                description = description)
                    step_recipe.save()
                
            return redirect('recipe_view', id = id)

        else:
            # Create FormsSet 
            form_steps = Steps_FormsSet()

            return render(request, "knitout/add_steps.html",{
                "form_steps": form_steps
            })
    except:
        return render(request, "knitout/error.html",{
            "message": "Something went wrong! Please try again."
        })
    
    
def recipe_view(request, id):
    try:
        recipe = get_object_or_404(Recipe, id = id)
        
        return render(request, "knitout/recipe.html", {
            "recipe": recipe
        })
    except:
        return render(request, "knitout/error.html", {
            "message": "Cannot find given recipie. Please try again."
        })
    
def recipe_view_steps(request, id):
    # Get steps
    recipe = get_object_or_404(Recipe, id = id)
    steps = Step.objects.filter(recipe = recipe)
    
    return render(request, "knitout/recipe_steps.html",{
        "steps": steps
    })

def profile_view(request, username):

    if request.method == "GET":
        user = get_object_or_404(User, username = username)

        # Get name
        name = user.username

        # Get followers TODO
        followers = 0

        # Get number of recipies added by user
        if Recipe.objects.filter(user = user):
            num_recipes = len(Recipe.objects.filter(user = user))
        else:
            num_recipes = 0

        # Get date user joined 
        joined = user.date_joined
        
        # Get recipes
        recipes = Recipe.objects.filter(user = user)

        # Check if profile belonges to logged in user
        owner = False
        if user == request.user:
            owner = True

        # Create profile
        profile = {
            "name": name,
            "followers": followers,
            "num_recipes": num_recipes,
            "joined": joined,
            "recipes": recipes,
            "owner": owner
        }

        return render (request, "knitout/profile.html", {
            "profile": profile
        })
    
@login_required
def favorites_view(request):
    try:
        recipes = Recipe.objects.filter(favorites = request.user)

        return render (request, "knitout/favorites.html", {
            "recipes": recipes
        })
    except:
        return render(request, "knitout/error.html",{
            "message": "Something went wrong! Please try again."
        })
    
@login_required
def following_view(request):
    followed_users = get_object_or_404(Follow, user = request.user).followed_users.all()
    if len(followed_users) == 0:
        followed_users_recipes = False
    else:
        followed_users_recipes = {}
        for user in followed_users:
            recipes = Recipe.objects.filter(user = user).order_by('-date')
            followed_users_recipes[user] = recipes
        
        
    
    return render(request, "knitout/following.html", {
        "followed_users_recipes": followed_users_recipes
    })



'''API likes/dislikes, favorites, follow'''
@csrf_exempt
def likes(request, id):
    try:
        recipe = get_object_or_404(Recipe, id = id)

        # If GET the get likes and dislikes
        if request.method == "GET":
            # Get number of likes and dislikes
            num_likes = len(recipe.likes.all())
            num_dislikes = len(recipe.dislikes.all())

            # Calculate procentege of likes
            if num_likes == 0 and num_dislikes == 0:
                procent_likes = 50
            elif num_likes == 0:
                procent_likes = 0
            elif num_dislikes == 0:
                procent_likes = 100
            else:
                procent_likes = num_likes / (num_likes + num_dislikes) * 100

            liked = False
            disliked = False
            logged = False

            # Check if logged in and if liked/disliked already
            if request.user.is_authenticated:
                logged = True
                if recipe.likes.filter(username = request.user).exists():
                    liked = True
                if recipe.dislikes.filter(username = request.user).exists():
                    disliked = True
            
            # Create response data and send vis JsonResponse
            response_data = {"procent_likes": procent_likes,
                             "liked": liked,
                             "disliked": disliked,
                             "logged": logged}
            
            return JsonResponse(response_data)


        if request.method == "PUT":
            # Check if logged in and if liked/disliked already
            if request.user.is_authenticated:
                # If liked => Unlike
                if recipe.likes.filter(username = request.user).exists():
                    recipe.likes.remove(request.user) 
                    return JsonResponse ({"message": "Unliked"})                      
                else:
                    #  Like and check if Disliked
                    recipe.likes.add(request.user)
                    if recipe.dislikes.filter(username = request.user).exists():
                        recipe.dislikes.remove(request.user)
                    return JsonResponse ({"message": "Liked"})
    
    except:
        return render(request, "knitout/error.html", {
            "message": "Something went wrong! Please try again."
        })
                                               

@csrf_exempt
def dislikes(request, id):
    try:
        recipe = get_object_or_404(Recipe, id = id)

        if request.method == "PUT":
            # Check if logged in and if liked/disliked already
            if request.user.is_authenticated:
                # If Disliked => Undisliked
                if recipe.dislikes.filter(username = request.user).exists():
                    recipe.dislikes.remove(request.user) 
                    return JsonResponse ({"message": "Undisliked"})                      
                else:
                    #  Disike and check if Liked
                    recipe.dislikes.add(request.user)
                    if recipe.likes.filter(username = request.user).exists():
                        recipe.likes.remove(request.user)
                    return JsonResponse ({"message": "Disliked"})
    except:
        return render(request, "knitout/error.html", {
            "message": "Something went wrong! Please try again."
        })
    

@csrf_exempt     
def favorites(request, id):
    recipe = get_object_or_404(Recipe, id = id)

    if request.method == "GET":
        # Check if logged and favorited
        logged = False
        favorited = False
        if request.user.is_authenticated:
            logged = True
            if recipe.favorites.filter(username = request.user).exists():
                favorited = True

        # Create a response_data and send via JsonResponse
        response_data = {
            "logged": logged,
            "favorited": favorited
        }

        return JsonResponse(response_data)


    if request.method == "PUT":
        # Check if logged in and if already in favroites
        if request.user.is_authenticated:
            # If in favorites then remove
            if recipe.favorites.filter(username = request.user):
                recipe.favorites.remove(request.user)
                return JsonResponse({"message": "Unfavorited"})
            # If not in favorites than add
            else:
                recipe.favorites.add(request.user)
                return JsonResponse({"message": "Favorited"})
            
@csrf_exempt
def follow(request, username):
    # Check if logged in
    if request.user.is_authenticated == False:
        message = "Guest"
        return JsonResponse({"message": message})
    
    # User to follow
    user = get_object_or_404(User, username = username)  

    if request.method == "GET":
        # Check if Followed/Unfollowed
        if Follow.objects.filter(user=request.user, followed_users=user).exists():
            message = "Followed"
        else:
            message = "Unfollowed"

        return JsonResponse({"message": message})

    
    if request.method == "PUT":
        # If followed then unfollow
        if Follow.objects.filter(user=request.user, followed_users=user).exists():
            follow = Follow.objects.get(user=request.user)
            follow.followed_users.remove(user)
            message = "Unfollowed"
        # If unfollowed then follow
        else:
            follow, created = Follow.objects.get_or_create(user=request.user)
            follow.followed_users.add(user)
            message = "Followed"

        return JsonResponse({"message": message})    
            
