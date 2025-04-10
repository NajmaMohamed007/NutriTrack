from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        result = float(value) / float(arg)
        return round(result, 2)  # Optional rounding
    except (ValueError, ZeroDivisionError, TypeError):
        return 0  # Or return "N/A", depending on your needs

@register.filter
def mul(value, arg):
    try:
        result = float(value) * float(arg)
        return round(result, 2)
    except (ValueError, TypeError):
        return 0
