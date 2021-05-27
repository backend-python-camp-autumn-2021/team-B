
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import home_page,header,footer
from cart.api import CartdetailView 

urlpatterns = [

    # app
    path('eshop_accounts/', include('eshop_accounts.urls', namespace='eshop_accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('comment/', include('comment.urls')),
    path('cart-detail/<int:pk>',CartdetailView.as_view() ,name='cartitem-detail'),
    
    
    # home
    path('', home_page, name='home'),
    path('header', header, name="header"),
    path('footer', footer, name="footer"),
    # admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # add root static files
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # add media static files
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)