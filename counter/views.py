from django.shortcuts import render
import requests
from django.conf import settings
import urllib.parse
from difflib import get_close_matches

# Sample valid food terms (expand this later or fetch dynamically)
VALID_FOODS = [
    "apple", "banana", "chicken breast", "pasta", "rice", "broccoli",
    "salmon", "beef", "carrot", "cheese", "fries", "brisket", "yogurt",
    "pizza", "lettuce", "grapes", "oatmeal", "egg", "cucumber", "potato"
]

# Landing Page View
def home_page(request):
    return render(request, 'home_page.html')

# Home View with error + suggestion handling
def home(request):
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
                return render(request, 'home.html', {
                    'api': "oops! There was an error",
                    'query': query
                })

    # Handle if everything was invalid
    if query and not data:
        suggestion_list = []
        for food in invalid_inputs:
            matches = get_close_matches(food.lower(), VALID_FOODS, n=2, cutoff=0.5)
            suggestion_list.extend(matches)

        return render(request, 'home.html', {
            'api': "invalid",
            'query': query,
            'suggestions': list(set(suggestion_list))  # Remove duplicates
        })

    return render(request, 'home.html', {
        'api': data,
        'query': query
    })

# About View (unchanged)
def about(request):
    return render(request, 'about.html')
