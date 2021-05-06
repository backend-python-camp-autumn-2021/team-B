from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, Http404
# Create your views here.
from cart.forms import UserNewOrderForm
from products.models import Cart,Product,CartItem



 
@login_required
def add_to_cart(request,product_id):
   
    new_order_form = UserNewOrderForm(request.POST or None)
    if new_order_form.is_valid():
        count = new_order_form.cleaned_data.get('count')
        user=request.user
        cart, created = Cart.objects.get_or_create(user=user, status='open')
        product = get_object_or_404(Product,id=product_id)
        cart_item, created2 = CartItem.objects.get_or_create(products=product, cart=cart)
        cart_item.quantity += int(count)
        cart_item.save()
    return redirect('/')

    