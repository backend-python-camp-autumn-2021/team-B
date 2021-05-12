from django import template

register = template.Library()

@register.filter
def aa(price,off):
    return price - off