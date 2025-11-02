from django.urls import path
from . import views

urlpatterns = [
    path('', views.champion_search_page, name='champion_search_page'),
    path('search/', views.search_champions, name='search_champions'),
]
