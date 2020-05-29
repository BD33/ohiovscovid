from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-about'),
    path('about/', views.about, name='covid-about'),

]