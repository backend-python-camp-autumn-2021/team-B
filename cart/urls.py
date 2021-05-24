from django.urls import path
from . import views
from .api import CartViewSet,CartListViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('cartitem',CartListViewSet,basename='cartitem')
app_name = 'cart'
urlpatterns = [
    path('add-to-cart/<product_id>', views.add_to_cart, name='add-to-cart'),
    path('show-order', views.show_order, name='show-order'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart-remove'),

]
urlpatterns+=router.urls
