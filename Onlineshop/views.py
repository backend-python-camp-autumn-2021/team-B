import itertools
from django.shortcuts import render, redirect
from sliders.models import Slider
from products.models import Product, Category
from contact.models import SiteSetting
from cart.forms import AddToCartForm


# header 
def header(request, *args, **kwargs):
    context = {
        'title': 'this is title'
    }
    return render(request, 'shared/Header.html', context)


# footer 
def footer(request, *args, **kwargs):
    context = {
        "about_us": "سایت فروشگاهی با جنگو"
    }
    return render(request, 'shared/Footer.html', context)

def my_grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def home_page(request):
    products = Product.objects.all()
    sliders = Slider.objects.all()
    most_visit_products = products.order_by('-visit_count').all()[:8]
    latest_products = products.order_by('-created').all()[:8]
    form = AddToCartForm()
    categories = Category.objects.all()
    if request.GET.get('c_q'):
        q = request.GET.get('c_q')
        pr_cats = products.filter(Categories__pk=q)
        print(pr_cats)
    else:
        pr_cats = products.filter(Categories__pk=1)

    context = {
        'data': 'این سایت فروشگاهی با فریم ورک django نوشته شده',
        'sliders': sliders,
        'most_visit': my_grouper(4, most_visit_products),
        'latest_products': my_grouper(4, latest_products),
        'form': form,
        'cats': categories,
        'pr_cats': pr_cats
    }
    return render(request, 'home_page.html', context)


def about_page(request):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request, 'about_page.html', context)