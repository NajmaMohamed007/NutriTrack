from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
from django import forms
import requests
from django.conf import settings
import urllib.parse
from django.template import loader
from difflib import get_close_matches
from django.core.exceptions import ObjectDoesNotExist
from .models import FoodLog  # Added import for FoodLog model
from django.http import HttpResponse
from django.utils import timezone
from .models import WaterIntake  # Make sure WaterIntake model is imported

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

# Food Logging Views
@login_required
def log_food(request):
    if request.method == 'POST':
        FoodLog.objects.create(
            user=request.user,
            food_name=request.POST.get('food_name'),
            calories=float(request.POST.get('calories')),
            protein=float(request.POST.get('protein')),
            carbs=float(request.POST.get('carbs')),
            fat=float(request.POST.get('fat')),
            amount=float(request.POST.get('amount')),
            meal_time=request.POST.get('meal_time', 'snack')  # Default to snack
        )
        messages.success(request, "Food logged successfully!")
        return redirect('dashboard')
    return redirect('home')


def food_log_view(request):
    # Add your view logic here to show all logged foods
    return render(request, 'counter/food_log.html')  # Cr
    

@login_required
def dashboard_view(request):
    # Calculate totals
    today = timezone.now().date()
    foods = FoodLog.objects.filter(user=request.user, date__date=today)
    
    totals = {
        'calories': sum(f.calories for f in foods),
        'protein': sum(f.protein for f in foods),
        'carbs': sum(f.carbs for f in foods),
        'fat': sum(f.fat for f in foods),
        'water': request.user.waterintake_set.filter(date=today).count()
    }
    
    # Get goals from user profile
    try:
        profile = request.user.profile
        goals = {
            'calories': profile.calorie_goal,
            'protein': profile.protein_goal,
            'carbs': profile.carb_goal,
            'fat': profile.fat_goal
        }
    except:
        goals = {
            'calories': 2000,
            'protein': 50,
            'carbs': 300,
            'fat': 70
        }
    
    # Calculate percentages
    percentages = {
        'calories': min(100, int((totals['calories'] / goals['calories']) * 100)) if goals['calories'] else 0,
        # Add other macros as needed...
    }
    
    return render(request, 'counter/dashboard.html', {
        'total_calories': totals['calories'],
        'calorie_goal': goals['calories'],
        'calorie_percentage': percentages['calories'],
        # Add other macros similarly
        'water_glasses': totals['water'],
        'recent_foods': FoodLog.objects.filter(user=request.user).order_by('-date')[:3]
    })

@login_required
def log_water(request):
    if request.method == 'POST':
        WaterIntake.objects.create(user=request.user)
        messages.success(request, "Water logged successfully!")
    return redirect('dashboard')

# Authentication Views
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
    
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_setup_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        from .models import Profile
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'counter/profile_setup.html', {'form': form})

# Core Application Views
def home_page_view(request):
    return render(request, 'home_page.html')

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
                return render(request, 'counter/home.html', {
                    'api': None,
                    'query': query,
                    'error_message': str(e)
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

def test_view(request):
    return HttpResponse("RAW TEST OUTPUT - If you see this, routing works")

def about_view(request):
    return render(request, 'about.html')

@login_required
def tips_view(request):
    return render(request, 'tips.html')

@login_required
def calculator_view(request):
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

            bmi = weight / ((height / 100) ** 2)
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
