from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, Http404
from django.urls import reverse
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
        # product = Product.objects.filter(id=product_id)
        cart_item, created2 = CartItem.objects.get_or_create(products=product, cart=cart)
        cart_item.quantity += int(count)
        cart_item.save()
        return redirect(reverse("cart:show-order"))
        
    return redirect('/')


@login_required
def show_order(request, *args, **kwargs):

    context = {
        'order': None,
        'details': None,
        'total': 0
    }
    # user = request.user
    # open_order = user.carts.filter(status='open')
    open_order = Cart.objects.filter(user = request.user, status='open').first()
   
    if open_order is not None:
        context['order'] = open_order
        
        context['details'] = open_order.items.all()
        context['total'] = open_order.get_total_price()

    return render(request, 'cart/cart.html', context)


def cart_remove(request, product_id):
    # cart_item = CartItem.objects.filter(id=product_id)
    cart_item = get_object_or_404(CartItem, id=product_id)
    cart_item.delete()
    return redirect(reverse("cart:show-order"))   


