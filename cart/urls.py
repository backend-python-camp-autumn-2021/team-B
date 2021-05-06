from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
	path('add-to-cart/<product_id>', views.add_to_cart, name='add-to-cart'),
	
    # path('cart',views.cart, name='cart'),
    # path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),
	
	
]