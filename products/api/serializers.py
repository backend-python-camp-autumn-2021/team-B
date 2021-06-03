from django import forms
from django.utils import tree
from django.utils.translation import activate
from rest_framework import fields, serializers
from products.models import Category, Product


class ProductListSerializer(serializers.ModelSerializer):
    suplier = serializers.StringRelatedField(read_only=True)
    active =serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields =['id','title','description','image','brand',
            'price','active','suplier']
        

class ProductDetailSerializer(serializers.ModelSerializer):
    suplier = serializers.StringRelatedField(read_only=True)
    Categories = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['title','description','slug','suplier','Categories',
            'image','brand', 'price','active','discount','visit_count']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title', 'parent']
