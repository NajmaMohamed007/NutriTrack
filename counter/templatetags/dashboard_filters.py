from django import template

register = template.Library()

@register.filter
def calorie_percentage(consumed, goal):
    try:
        return min(int((consumed / goal) * 100), 100)
    except:
        return 0

@register.filter
def water_percentage(intake):
    return min(int((intake / 8) * 100), 100)

@register.filter 
def activity_percentage(minutes):
    return min(int((minutes / 60) * 100), 100)

@register.filter
def meal_icon(meal_time):
    icons = {
        'Breakfast': 'sun',
        'Lunch': 'sun',
        'Dinner': 'moon',
        'Snack': 'cookie'
    }
    return icons.get(meal_time, 'utensils')