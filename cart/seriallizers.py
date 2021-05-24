from django.apps import apps
from rest_framework import serializers

Cart = apps.get_model('products', 'Cart')
CartItem=apps.get_model('products','CartItem')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields='__all__'





