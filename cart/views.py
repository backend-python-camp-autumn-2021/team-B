from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.urls.base import reverse_lazy
from cart.forms import AddToCartForm
from products.models import Cart,Product,CartItem
# payment
from django.http import HttpResponse,Http404
from django.shortcuts import redirect
from zeep import Client

@login_required(login_url=reverse_lazy('eshop_accounts:login'))
def add_to_cart(request,product_id):
    form = AddToCartForm(request.POST or None)
    if form.is_valid():
        cart, created = Cart.objects.get_or_create(user=request.user, status='open')
        product = get_object_or_404(Product,id=product_id)
        count = form.cleaned_data.get('count')       
        if count < 0:
            count = 1        
        user=request.user
        # product = Product.objects.filter(id=product_id)
        cart_item, created2 = CartItem.objects.get_or_create(products=product, cart=cart)
        cart_item.quantity += int(count)
        cart_item.save()
        return redirect(reverse_lazy('cart:show-order'))
        
    return redirect('/')


@login_required(login_url=reverse_lazy('eshop_accounts:login'))
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

# payment

MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
amount = 1000  # Toman / Required
description = "پرداخت آنلاین شاپ"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional

client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify/'  # Important: need to edit for realy server.



def send_request(request, *args, **kwargs):
    total_price = 0
    open_order = Cart.objects.filter(user = request.user, status='open').first()
   
    if open_order is not None:
        total_price = open_order.get_total_price()
        result = client.service.PaymentRequest(
            MERCHANT, total_price, description, email, mobile, f"{CallbackURL}/{open_order.id}"
        )
        if result.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
          
        else:
            return HttpResponse('Error code: ' + str(result.Status))
    raise Http404()



def verify(request, *args, **kwargs):
    order_id = kwargs.get('order_id')
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
          
            user_order = Cart.objects.get(id=order_id)
            user_order.status = ( 'closed',)
            user_order.save()
            return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')




