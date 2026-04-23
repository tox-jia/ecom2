from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))


@register.filter
def get_question(term, lang):
    return term.get_question(lang)