# templatetags/custom_filters.py

from django import template
import re

register = template.Library()

@register.filter(name='remove_numbers')
def remove_numbers(value):
    return re.sub(r'\d+', '', value)  # Remove all numbers
