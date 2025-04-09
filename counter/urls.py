from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Landing page URL
    path('home/', views.home, name='home'),  # Home page URL
    path('about/', views.about, name='about'),
]
