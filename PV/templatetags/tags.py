from django import template
from django.template.loader import get_template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return

users_template = get_template('base_results.html')
register.inclusion_tag(users_template)(active)