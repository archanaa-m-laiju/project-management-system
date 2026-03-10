from django import template

register = template.Library()

@register.filter
def dict_first_value(dictionary):
    """Return the first value from a dictionary"""
    if dictionary:
        return next(iter(dictionary.values()), None)
    return None
