
from django.shortcuts import render
import requests  # Move the import to the top of the file
# Home view
def home(request):
    query = '1lb brisket and fries'
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': 'YafOS7OCePWnFhZJcVhJhag==YWgVwbaWh1rNIOO7'})  # Make sure to replace with actual API key

    if response.status_code == requests.codes.ok:
        data = response.json()  # Parse the JSON data from the response
        print(data)  # Optional: print the data to see it in the console (for debugging)
    else:
        print("Error:", response.status_code, response.text)
        data = None  # If the request fails, set data to None

    return render(request, 'home.html', {'data': data})  # Pass the data to the template

# About view
def about(request):
    return render(request, 'about.html')

