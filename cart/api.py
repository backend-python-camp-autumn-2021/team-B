from rest_framework.views import APIView
from rest_framework import viewsets
from .seriallizers import CartItemSerializer,CartSerializer,CartItemDetailSerializer
from django.apps import apps
from rest_framework.viewsets import ReadOnlyModelViewSet
Cart = apps.get_model('products', 'Cart')
CartItem=apps.get_model('products','CartItem')
from .seriallizers import CartItemSerializer,CartSerializer
from rest_framework import generics





class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartListViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


# class ShowCartItem(ReadOnlyModelViewSet):
#     queryset = CartItem.objects.all()
#
#     serializers={
#         "list":CartItemSerializer,
#         'retrieve':CartSerializer
#     }
#
#     def get_serializer_class(self):
#         return self.serializers.get(self.action)
class CartdetailView(generics.RetrieveAPIView):
    queryset=CartItem.objects.all()
    serializer_class=CartItemDetailSerializer

    