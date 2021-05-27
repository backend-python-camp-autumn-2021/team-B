from django.apps import apps
from django.contrib.auth import models
from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

Cart = apps.get_model('products', 'Cart')
CartItem=apps.get_model('products','CartItem')
Product=apps.get_model('products','Product')
# User=apps.get_model("products",'User')


class UserCart(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=["user"]



class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["title"]


class CartSerializer(serializers.ModelSerializer):
    carts=serializers.StringRelatedField(read_only=True)
    user=serializers.StringRelatedField(read_only=True)


    class Meta:
        model=Cart
        fields='__all__'


class CartItemSerializer(serializers.ModelSerializer):
    products=serializers.HyperlinkedRelatedField(view_name='products:product-detail', read_only=True)
    # items=serializers.StringRelatedField(read_only=True)

    

    class Meta:
        model=CartItem
        fields=['quantity','products','cart','url']


class CartItemDetailSerializer(serializers.ModelSerializer):


    class Meta:
        model=CartItem
        fields='__all__'



