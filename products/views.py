from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView,DetailView
from .models import Product,Category
from cart.forms import UserNewOrderForm

# class
class ProductsList(ListView):
    model = Product
    template_name = 'products/products_list.html'
    # context_object_name = 'a_products'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.filter(active=True)


class SearchProductsView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    # context_object_name = 'a_products'
    paginate_by = 6

    def get_queryset(self):
        request = self.request
        print(request.GET)
        query = request.GET.get('q')
        # category = request.GET.get('category')
        if query is not None:
            return Product.objects.filter(active=True, title__icontains=query)
        
        # if category is not None:
        #     return Product.objects.filter(active=True, Categories_id=category)
        return Product.objects.filter(active=True)

# all category
# class ProductsListByCategory(ListView):
#     model = Product
#     template_name = 'products/products_list.html'
#     paginate_by = 6
#     context_object_name = 'a_products'

#     def get_queryset(self):
#          return Product.objects.all()

class ProductsListByCategory(ListView):
    model = Product
    template_name = 'products/products_list.html'
    paginate_by = 6
    # context_object_name = 'a_products'

    def get_queryset(self):
        print(self.kwargs)
        # http://127.0.0.1:8000/products/products/کتاب-ولوازم-التحریر
        # {'Category_title': 'کتاب-ولوازم-التحریر'}
        category_title = self.kwargs['Category_title']
        # print(category_title)
        category = Category.objects.filter(title__iexact=category_title).first()
        print(category)
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
   
        return Product.objects.filter(Categories__title__iexact=category_title, active=True)

class ProductsDetail(DetailView):
    
    model = Product
    template_name = "products/product_detail.html"
    # context_object_name = 'a_product'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['new_order_form'] = UserNewOrderForm()
        return context

      
def products_categories_partial(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/products_categories_partial.html', context)

    
	 
