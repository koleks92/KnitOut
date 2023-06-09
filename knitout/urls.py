from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        # INDEX/SEARCH
        path("", views.index, name="index"),
        path("search", views.search, name="search"),
        # USER RELATED
        path("login", views.login_view, name="login"),
        path("register", views.register, name="register"),
        path("logout", views.logout_view, name="logout"),
        path("profile/<str:username>", views.profile_view, name="profile_view"),
        # ADD RECIPE
        path("add_recipe", views.add_recipe, name="add_recipe"),
        path("add_recipe/<int:id>/steps", views.add_steps, name="add_steps"),
        # VIEW RECIPE
        path("recipe/<int:id>", views.recipe_view, name="recipe_view"),
        path("recipe/<int:id>/steps", views.recipe_view_steps, name="recipe_view_steps"),
        # APIS
        path("likes/<int:id>", views.likes, name="likes"),
        path("dislikes/<int:id>", views.dislikes, name="dislikes"),
        path("favorites/<int:id>", views.favorites, name="favorites"),
        path("follow/<str:username>", views.follow, name="follow"),
        path("bookmark/<int:id>/<int:step>", views.bookmark, name="bookmark"),
        path("edit/<int:id>/<int:step>", views.edit, name="edit"),
        # REST
        path("favorites", views.favorites_view, name="favorites_view"),
        path("following", views.following_view, name="following_view"),
        path("by_difficulty", views.by_difficulty, name="by_difficulty"),
        path("by_type", views.by_type, name="by_type")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)