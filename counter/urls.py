from django.urls import path
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home_page_view, name='home_page'),  # first oage
    path('home/', views.home_view, name='home'), 
    path('about/', views.about_view, name='about'),
    path('tips/', views.tips_view, name='tips'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/setup/', views.profile_setup_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('log-food/', views.log_food, name='log_food'),
     path('food-log/', views.food_log_view, name='food_log'),
    path('admin/', admin.site.urls),
    path('log-water/', views.log_water, name='log_water'),
    path('update-goal/', views.update_goal, name='update_goal'),
    
]