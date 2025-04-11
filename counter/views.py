from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.conf import settings
import urllib.parse
from difflib import get_close_matches
from .forms import CustomUserCreationForm, ProfileForm
from .models import CustomUser

# Sample valid food terms
VALID_FOODS = [
    "apple", "banana", "chicken breast", "pasta", "rice", "broccoli",
    "salmon", "beef", "carrot", "cheese", "fries", "brisket", "yogurt",
    "pizza", "lettuce", "grapes", "oatmeal", "egg", "cucumber", "potato"
]

# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Complete your profile.")
            return redirect('profile_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect('home')

@login_required
def profile_setup_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile/setup.html', {'form': form})

# Core Application Views
@login_required
def dashboard_view(request):
    # Get user's recent food entries (you'll need to implement this model)
    recent_foods = []  # Replace with actual query
    return render(request, 'dashboard.html', {
        'user': request.user,
        'recent_foods': recent_foods
    })

def home_page_view(request):
    return render(request, 'home_page.html')

@login_required
def home_view(request):
    data = []
    query = ""
    invalid_inputs = []
    suggestions = []

    if request.method == "POST":
        query = request.POST.get('query', '').strip()
    else:
        query = request.GET.get('query', '').strip()

    if query:
        foods = query.split(",")

        for food in foods:
            original_food = food.strip()
            encoded_food = urllib.parse.quote(original_food)
            api_url = f"https://api.api-ninjas.com/v1/nutrition?query={encoded_food}"
            headers = {'X-Api-Key': settings.NUTRITION_API_KEY}

            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()
                result = response.json()

                if result:
                    data.extend(result)
                    # Save to user's history if logged in
                    if request.user.is_authenticated:
                        pass  # Implement food history saving
                else:
                    invalid_inputs.append(original_food)
            except requests.exceptions.RequestException as e:
                messages.error(request, "There was an error fetching nutrition data.")
                return render(request, 'home.html', {
                    'api': "oops! There was an error",
                    'query': query
                })

    if query and not data:
        suggestion_list = []
        for food in invalid_inputs:
            matches = get_close_matches(food.lower(), VALID_FOODS, n=2, cutoff=0.5)
            suggestion_list.extend(matches)

        messages.info(request, "We couldn't find some foods. Try these suggestions!")
        return render(request, 'home.html', {
            'api': "invalid",
            'query': query,
            'suggestions': list(set(suggestion_list))
        })

    return render(request, 'home.html', {
        'api': data,
        'query': query
    })

def about_view(request):
    return render(request, 'about.html')

def tips_view(request):
    return render(request, 'tips.html')

@login_required
def calculator_view(request):
    # Pre-fill with user data if available
    user_data = {
        'age': request.user.age,
        'weight': request.user.weight,
        'height': request.user.height,
        'gender': request.user.gender
    }
    return render(request, 'calculator.html', {'user_data': user_data})

# Password reset views would go here (use Django's built-in views)