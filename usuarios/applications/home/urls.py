from django.contrib import admin
from django.urls import path

from . import views

app_name = 'home_app'

urlpatterns = [
    path('home/', views.IndexHomeView.as_view(), name='home'), 
      
]