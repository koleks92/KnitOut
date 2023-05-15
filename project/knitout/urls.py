from django.urls import path
from . import views

urlpatterns = [
        path("", views.index, name="index"),
        path("login", views.login_view, name="login"),
        path("register", views.register, name="register"),
        path("logout", views.logout_view, name="logout"),
        path("add_recipe", views.add_recipe, name="add_recipe"),
        path("add_recipe/<int:id>/steps", views.add_steps, name="add_steps"),
        path("recipe/<int:id>", views.recipe_view, name="recipe_view"),
        path("recipe/<int:id>/steps", views.recipe_view_steps, name="recipe_view_steps"),
        path("likes/<int:id>", views.likes, name="likes"),
        path("dislikes/<int:id>", views.dislikes, name="dislikes"),
        path("favorites/<int:id>", views.favorites, name="favorites"),
        path("profile/<str:username>", views.profile_view, name="profile_view")
]