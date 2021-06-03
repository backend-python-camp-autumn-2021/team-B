from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
    path('add-to-cart/<product_id>', views.add_to_cart, name='add-to-cart'),
    path('show-order', views.show_order, name='show-order'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart-remove'),
    path('send-request/', views.send_request, name='send-request'),
    path('verify/<order_id>',views. verify, name='verify'),

]