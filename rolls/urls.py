"""
Rolls app urls
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

app_name = 'rolls'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('detail/<int:awesome>/', views.DetailView.as_view(), name='detail'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]
