from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, Http404
# Create your views here.
from cart.forms import UserNewOrderForm
from products.models import Cart,Product

@login_required
def add_to_cart(request):
    new_order_form = UserNewOrderForm(request.POST or None)
    
    if new_order_form.is_valid():
        cart, created = Cart.objects.get_or_create(user=user, status='open')
        product_id = new_order_form.cleaned_data.get('product_id')
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1
        product = get_object_or_404(Product,product_id=product_id)
        cart_item, created2 = CartItem.objects.get_or_create(product_id=product.id, count=count)
        cart_item.quantity += 1
        cart_item.save()
        # cart.cartitem_set.create(product_id=product.id, price=product.price, count=count)
        # todo: redirect user to user panel
        # return redirect('/user/orders')
        return redirect(f'/products/{product.id}/{product.title.replace(" ", "-")}')

    return redirect('/')

def cart(request):
    user = request.user
    cart_obj = user.carts.filter(status='open')
    if cart_obj:
        return render(request, 'cart.html', {'cart_items': cart_obj[0].items.all()})
    else:
        return render(request, 'cart.html', {'error': 'You have any cart.'})



def remove_from_cart(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
        return HttpResponseRedirect(reverse('cart'))



