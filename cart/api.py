from rest_framework.views import APIView
from rest_framework import viewsets
from .seriallizers import CartItemSerializer,CartSerializer
from django.apps import apps
Cart = apps.get_model('products', 'Cart')
CartItem=apps.get_model('products','CartItem')


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartListViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
