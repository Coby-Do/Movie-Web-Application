from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html')),
    path('add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist')
]