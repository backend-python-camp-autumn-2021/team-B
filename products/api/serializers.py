from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from products.models import Product, ProductsDetail, Category, Store


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['slug']


# class ProductListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         exclude = ['slug']


# class ProductDetailSerializer(HyperlinkedModelSerializer):
#     products = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = ProductsDetail
#         exclude = ['id']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    Categories = serializers.StringRelatedField(read_only = True)
    suplier = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Product
        fields = ["id", "title", "description","slug", "image", "brand", "price", "active", "created", "updated", "discount", "Categories", "suplier"]
