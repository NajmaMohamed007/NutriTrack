from django.shortcuts import render
import json
import requests
from django.conf import settings  # To use Django settings for API key

# Home view
def home(request):
    data = None  # Initialize data variable
    query = request.GET.get('query', '').strip()  # Get user input safely and strip whitespace

    if not query:
        query = '1lb brisket and fries'  # Default query

    # API request to get nutrition data
    api_url = f'https://api.api-ninjas.com/v1/nutrition?query={query}'
    headers = {'X-Api-Key': settings.NUTRITION_API_KEY}  # Correct header format

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)

        if response.status_code == 200:
            data = response.json()
            if not data:
                data = [{"name": "Unknown Food", "calories": "N/A"}]
        else:
            data = [{"name": "Error", "calories": "N/A", "message": response.text}]  # Handle error responses

    except requests.exceptions.RequestException as e:
        data = [{"name": "Error", "calories": "N/A", "message": str(e)}]  # Handle request errors

    return render(request, 'home.html', {'api': data})  # Pass the API data to the template

# About view
def about(request):
    return render(request, 'about.html')
