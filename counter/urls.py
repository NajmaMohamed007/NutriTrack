from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page_view, name='home_page'),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('tips/', views.tips_view, name='tips'),
    path('calculator/', views.calculator_view, name='calculator'),
    
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_setup_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]