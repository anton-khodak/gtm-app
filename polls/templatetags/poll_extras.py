from django import template
from django.template.defaultfilters import urlize

register = template.Library()


@register.filter
def urlize_and_render_image(text):
    text = urlize(text)
    return text.replace('{{', '<img width="100%" src="').replace('}}', '">')