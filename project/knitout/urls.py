from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.login_view, name="login"),
        path("register", views.register, name="register"),
        path("logout", views.logout_view, name="logout"),
        path("add_recipe", views.add_recipe, name="add_recipe"),
        path("add_recipe/<int:id>/steps", views.add_steps, name="add_steps"),
        path("<int:id>", views.recipe_view, name="recipe_view"),
        path("<int:id>/steps", views.recipe_view_steps, name="recipe_view_steps"),
]