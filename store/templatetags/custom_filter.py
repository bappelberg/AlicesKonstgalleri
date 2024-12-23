from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    """Converts a number to a currency format by prefixing 'kr'."""
    try:
        return str(number) + ' kr'
    except TypeError:
        return number  # Return the original value if there is a type error

@register.filter(name='multiply')
def multiply(number, number1):
    """Multiplies two numbers."""
    try:
        return number * number1
    except (TypeError, ValueError):
        return 0  # Return 0 in case of invalid inputs
