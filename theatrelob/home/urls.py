from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.index, name='index'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html')),
    path('add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('get_access_token', views.get_access_token, name='get_access_token'),
    path('randomrec/', views.randomrec, name='Random Movie Recommendation'),
    # Handling profiles and badges
    path('logout/', logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('badge_list/', views.badge_list, name='badge_list'),
    path('watch_movie/', views.watch_movie, name='watch_movie'),
    path('create_badges/', views.create_badges, name='create_badges'),
    path('reset_user_badges/', views.reset_user_badges, name='reset_user_badges'),
    path('delete_badges/', views.delete_badges, name='delete_badges'),
    path('watch_animation/', views.watch_animation, name='watch_animation'),
    path('watch_documentary/', views.watch_documentary, name='watch_documentary'),
    path('watch_action/', views.watch_action, name='watch_action'),
    path('watch_comedy/', views.watch_comedy, name='watch_comedy'),
    path('watch_romance/', views.watch_romance, name='watch_romance'),
    # For Recommending Movies
    path('recommend_movie_view/', views.recommend_movie_view, name='recommendList'),
    path('movie_search_add/', views.movie_search_add, name='addedMovie'),
]

