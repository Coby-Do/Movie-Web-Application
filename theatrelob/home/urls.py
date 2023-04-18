from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html')),

    # For Watchlists
    path('watchlist/', views.watchlist, name='watchlist'),
    path('add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    path('get_access_token', views.get_access_token, name='get_access_token'),
    path('delete_access_token', views.delete_access_token, name='delete_access_token'),
    path('api/watch_movie', views.api_search_and_add, name='api_search_and_add'),
    # For Profiles, Logins, Logouts, Registrations
    path('logout/', logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # For Badges
    path('badge_list/', views.badge_list, name='badge_list'),
    path('create_badges/', views.create_badges, name='create_badges'),
    path('reset_user_badges/', views.reset_user_badges, name='reset_user_badges'),
    path('delete_badges/', views.delete_badges, name='delete_badges'),

    # For Recommending Movies
    path('randomrec/', views.randomrec, name='Random Movie Recommendation'),
    path('recommend_movie_view/', views.recommend_movie_view, name='recommendList'),
    path('movie_search_add/', views.movie_search_add, name='addedMovie'),
]

