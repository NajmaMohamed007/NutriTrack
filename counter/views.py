from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm
import requests
from django.conf import settings
import urllib.parse
from difflib import get_close_matches


# Sample valid food terms
VALID_FOODS = [
    "apple", "banana", "chicken breast", "pasta", "rice", "broccoli",
    "salmon", "beef", "carrot", "cheese", "fries", "brisket", "yogurt",
    "pizza", "lettuce", "grapes", "oatmeal", "egg", "cucumber", "potato"
]

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
        username = request.POST.get('username')  # Using .get() to avoid KeyError
        password = request.POST.get('password')  # Using .get() to avoid KeyError
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_setup_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile/setup.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

def home_page_view(request):
    return render(request, 'home_page.html')

@login_required
def home_view(request):
    data = []
    query = ""
    invalid_inputs = []
    suggestions = []

    # Get query from POST or GET request
    if request.method == "POST":
        query = request.POST.get('query', '').strip()
    else:
        query = request.GET.get('query', '').strip()

    if query:
        foods = query.split(",")
        
        # Iterate over foods to get their nutrition information
        for food in foods:
            original_food = food.strip()
            encoded_food = urllib.parse.quote(original_food)
            api_url = f"https://api.api-ninjas.com/v1/nutrition?query={encoded_food}"
            headers = {'X-Api-Key': settings.NUTRITION_API_KEY}

            try:
                response = requests.get(api_url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = response.json()

                print(f"API response for {original_food}: {result}")  # Print the response for debugging
                if result:
                    data.extend(result)
                else:
                    invalid_inputs.append(original_food)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching data: {e}")
                messages.error(request, "There was an error fetching nutrition data.")
                return render(request, 'home.html', {
                    'api': "oops! There was an error",
                    'query': query
                })

        if query and not data:
            # Find suggestions for invalid foods
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
