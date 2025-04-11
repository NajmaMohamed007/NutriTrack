from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Landing page URL
    path('home/', views.home, name='home'),  # Home page URL
    path('about/', views.about, name='about'),
    path('tips/', views.tips_view, name='tips'),
    path('calculator/', views.calculator_view, name='calculator'),
   path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

