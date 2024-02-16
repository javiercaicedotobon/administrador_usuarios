from django.contrib import admin
from django.urls import path

from . import views

app_name = 'users_app'

urlpatterns = [
    path('crear/', views.CreateUserView.as_view(), name='crear'), 
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('update/<pk>/', views.UserUpdateView.as_view(), name='update'), 
    path('allusers/', views.UserListView.as_view(), name='users_all'), 
    path('active/<pk>/', views.ActiveUser.as_view(), name='verificacion'), 
    path('update/', views.UpdatePasswordView.as_view(), name='update_password'), 
]