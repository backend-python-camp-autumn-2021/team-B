
# from . import serializers
from rest_framework import permissions, request
from eshop_accounts.models import Suplier
from .serializers import ProductListSerializer,ProductDetailSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet
# mixin
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from products.models import Product, Category
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status


class ProductViewSet(ModelViewSet):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'GET':
            suplier = Suplier.objects.filter(user=request.user)
            if suplier:
                if request.method != 'POST':
                    if suplier != self.get_object().suplier:
                        raise PermissionDenied('You Cant')
            else:
                raise PermissionDenied('You Cant')
        return super().dispatch(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     if self.request.method in ['GET', 'POST']:
    #         return ProductListSerializer
    #     return ProductDetail

class ProductList(ListCreateAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()


class CreateCategoryApiView(CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()