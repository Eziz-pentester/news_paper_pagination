# news/templatetags/custom_filters.py

from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска', 'дурак', 'глупец']  # список нежелательных слов

@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value
    pattern = r'\b(' + '|'.join(map(re.escape, BAD_WORDS)) + r')\b'
    return re.sub(pattern, lambda m: m.group(1)[0] + '*' * (len(m.group(1)) - 1), value, flags=re.IGNORECASE)
