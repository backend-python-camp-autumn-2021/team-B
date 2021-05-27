from django import template

register = template.Library()

@register.filter()
def length_range(price,off):
    return (price * off)/100