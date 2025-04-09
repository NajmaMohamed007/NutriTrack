from django.shortcuts import render
import json
import requests
from django.conf import settings
import urllib.parse

# Landing Page View
def home_page(request):
    return render(request, 'home_page.html')  # This renders the landing page

# Home view (existing)
def home(request):
    data = []
    query = ""

    if request.method == "POST":
        query = request.POST.get('query', '').strip()
    else:
        query = request.GET.get('query', '').strip()

    if not query:
        query = "brisket, fries"  # Default query

    foods = query.split(",")  # Allow multiple foods separated by commas

    for food in foods:
        food = urllib.parse.quote(food.strip())  # Encode food name
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query={food}"
        headers = {'X-Api-Key': settings.NUTRITION_API_KEY}

        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if result:
                data.extend(result)
            else:
                data.append({"name": food, "calories": "N/A"})
        except requests.exceptions.RequestException as e:
            data.append({"name": "Error", "calories": "N/A", "message": str(e)})

    return render(request, 'home.html', {'api': data, 'query': query})

# About view (existing)
def about(request):
    return render(request, 'about.html')
