from django import template

register = template.Library()


@register.filter(name='Censor')
def Censor(text):
    WORDS = [
        'баран',
        'петух',
        'осел',
    ]
    for word in WORDS:
        text = text.replace(word, '***')
    return text
