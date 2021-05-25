from django.apps import apps
from rest_framework import serializers

Cart = apps.get_model('products', 'Cart')
CartItem=apps.get_model('products','CartItem')
Product=apps.get_model('products','Product')




class ProductCartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["title"]


class CartSerializer(serializers.ModelSerializer):
    carts=serializers.StringRelatedField(read_only=True)

    class Meta:
        model=Cart
        fields='__all__'


class CartItemSerializer(serializers.HyperlinkedModelSerializer):
    cartproduct=serializers.StringRelatedField(read_only=True)
    items=serializers.StringRelatedField(many=True,read_only=True)

    class Meta:
        model=CartItem
        fields='__all__'




