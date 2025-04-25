from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        result = float(value) / float(arg)
        return round(result, 2)  
    except (ValueError, ZeroDivisionError, TypeError):
        return 0  

@register.filter
def mul(value, arg):
    try:
        result = float(value) * float(arg)
        return round(result, 2)
    except (ValueError, TypeError):
        return 0
