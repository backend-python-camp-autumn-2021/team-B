from django.urls import path
from rest_framework.decorators import api_view
from . import views
from .api import CartViewSet,CartListViewSet,CartdetailView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
router.register('cartitem',CartListViewSet,basename='cartitem')
app_name = 'cart'
urlpatterns = [
    path('add-to-cart/<product_id>', views.add_to_cart, name='add-to-cart'),
    path('show-order', views.show_order, name='show-order'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart-remove'),
    # path('cart-detail',CartdetailView.as_view,name='cart-detail')

]
urlpatterns+=router.urls

