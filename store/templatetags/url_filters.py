from django import template
register = template.Library()

# get the leading slash of the url
@register.filter
def strip_leading_slash(value):
    return value.lstrip('/')

# get the last character of the url string
@register.filter
def last_char(value):
    if value:
        return value[-1]
    return ''


@register.filter
def underscore_to_space(value):
    if isinstance(value, str):
        return value.replace('_', ' ')
    return value


@register.filter
def count_slashes(value):
    return value.count('/')


@register.filter
def char_count(value):
    return len(value)