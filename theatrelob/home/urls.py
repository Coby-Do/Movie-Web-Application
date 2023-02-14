from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from home.views import award_my_badge, award_tickets

urlpatterns = [
    path('', views.index, name='index'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='home/login.html')),
    path('add_to_watchlist', views.add_to_watchlist, name='add_to_watchlist'),
    # path('award_my_badge/', award_my_badge, name='award_my_badge'),
    # path('award_tickets/', award_tickets, name='award_tickets'),
    path('randomrec/', views.randomrec, name='Random Movie Recommendation'),
]
