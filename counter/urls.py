from django.urls import path
from . import views  # Import your views

urlpatterns = [
    # Redirect the root path to your home page
    path('', views.home_page_view, name='home_page'),  # This line handles the root path
    path('home/', views.home_view, name='home'),   # You can keep this or remove it if unnecessary
    path('about/', views.about_view, name='about'),
    path('tips/', views.tips_view, name='tips'),
    path('calculator/', views.calculator_view, name='calculator'),
  path('login/', views.login_view, name='login'),  # Changed from LoginView to login_view
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/setup/', views.profile_setup_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Other paths...
]
