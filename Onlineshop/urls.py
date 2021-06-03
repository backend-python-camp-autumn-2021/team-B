"""Onlineshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.urls.conf import re_path
from .views import home_page,header,footer,about_page

urlpatterns = [
    #api
    path('api-auth/', include('rest_framework.urls')),
    # app
    path('eshop_accounts/', include('eshop_accounts.urls', namespace='eshop_accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('comment/', include('comment.urls')),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings',)),  
    path('eshop_accounts/', include('allauth.urls')),  
    path('contact/', include('contact.urls')),  
    
    # home
    path('', home_page, name='home'),
    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    path('about-us', about_page, name="about_us"),
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)