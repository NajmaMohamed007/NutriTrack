from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django import forms
import requests
from django.conf import settings
import urllib.parse
from django.template import loader  # Add this import
from difflib import get_close_matches

# Sample valid food terms (adjust this list as needed)
VALID_FOODS = [
    "apple", "banana", "chicken breast", "pasta", "rice", "broccoli",
    "salmon", "beef", "carrot", "cheese", "fries", "brisket", "yogurt",
    "pizza", "lettuce", "grapes", "oatmeal", "egg", "cucumber", "potato"
]

# Calculator Form
class CalculatorForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=1)
    weight = forms.FloatField(label="Weight (kg)", min_value=1)
    height = forms.FloatField(label="Height (cm)", min_value=1)
    gender = forms.ChoiceField(label="Gender", choices=[('male', 'Male'), ('female', 'Female')])

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('profile_setup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'registration/login.html')  # or 'counter/login.html'

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_setup_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    try:
        profile = request.user.profile
    except profile.DoesNotExist:
        profile = profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'counter/profile/setup.html', {'form': form})


# Home Page View
def home_page_view(request):
    return render(request, 'home_page.html')

# Home View (for food search and suggestions)
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
                else:
                    invalid_inputs.append(original_food)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
                messages.error(request, "There was an error fetching nutrition data. Please try again.")
                return render(request, 'home.html', {
                    'api': None,  # No data returned on error
                    'query': query,
                    'error_message': str(e)  # Display the actual error message to help users
                })

        if query and not data:
            suggestion_list = []
            for food in invalid_inputs:
                matches = get_close_matches(food.lower(), VALID_FOODS, n=2, cutoff=0.5)
                suggestion_list.extend(matches)

            messages.info(request, "We couldn't find some foods. Try these suggestions!")
            return render(request, 'home.html', {
                'api': None,
                'query': query,
                'suggestions': list(set(suggestion_list))
            })

    return render(request, 'home.html', {
        'api': data,
        'query': query
    })


@login_required
def dashboard_view(request):
    print(f"DEBUG: User {request.user} authenticated")
    # Fixed template loader usage:
    template_path = loader.get_template('counter/dashboard.html').origin.name
    print(f"DEBUG: Template path: {template_path}")
    
    return render(request, 'counter/dashboard.html', {
        'force_visible': "THIS SHOULD APPEAR",
        'user': request.user  # Explicitly pass user
    })

from django.http import HttpResponse
def test_view(request):
    return HttpResponse("RAW TEST OUTPUT - If you see this, routing works")

# About View
def about_view(request):
    return render(request, 'about.html')

# Tips View
@login_required
def tips_view(request):
    return render(request, 'tips.html')

# Calculator View (for BMI and BMR calculation)
@login_required
def calculator_view(request):
    # Pre-fill with user data if available (optional, can be skipped if no need for pre-fill)
    user_data = {
        'age': request.user.age if request.user.is_authenticated else "",
        'weight': request.user.weight if request.user.is_authenticated else "",
        'height': request.user.height if request.user.is_authenticated else "",
        'gender': request.user.gender if request.user.is_authenticated else ""
    }

    if request.method == 'POST':
        form = CalculatorForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            gender = form.cleaned_data['gender']

            # Calculate BMI
            bmi = weight / ((height / 100) ** 2)

            # Calculate BMR using Mifflin-St Jeor equation
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            messages.success(request, f"BMI: {bmi:.2f}, BMR: {bmr:.2f}")
            return render(request, 'calculator.html', {
                'form': form,
                'user_data': user_data,
                'bmi': bmi,
                'bmr': bmr
            })
    else:
        form = CalculatorForm(initial=user_data)

    return render(request, 'calculator.html', {'form': form, 'user_data': user_data})

# Password Reset Views would go here (use Django's built-in views)
