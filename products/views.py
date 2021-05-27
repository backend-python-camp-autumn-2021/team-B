from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView,DetailView
from .models import Product,Category
from cart.forms import AddToCartForm



class ProductsList(ListView):
    model = Product
    template_name = 'products/products_list.html'    
    paginate_by = 6
                     
    def get_queryset(self):
        return Product.objects.filter(active=True)



class SearchProductsView(ListView):
    model = Product
    template_name = 'products/products_list.html'    
    paginate_by = 6

    def get_queryset(self):
        request = self.request
        # print(request.GET)
        query = request.GET.get('q')       
        if query is not None:
            return Product.objects.filter(active=True, title__icontains=query)       
        return Product.objects.filter(active=True)



class ProductsListByCategory(ListView):
    model = Product
    template_name = 'products/products_list.html'
    paginate_by = 6
    

    def get_queryset(self):        
        category_title = self.kwargs['Category_title']
        category = Category.objects.filter(title__iexact=category_title).first()        
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
   
        return Product.objects.filter(Categories__title__iexact=category_title, active=True)



class ProductsDetail(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    
    
    def get_object(self,queryset=None):
        object = super().get_object(queryset)
        pk = self.kwargs.get(self.pk_url_kwarg)
        if not self.request.session.get('views',None):
            self.request.session['views'] = [pk]

        if pk not in self.request.session.get('views',None):
            self.request.session['views'] += [pk]
            object.visit_count += 1 
            object.save()
        print( self.request.session['views'])    
        return object


    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['form'] = AddToCartForm()
        return context

      
def products_categories_partial(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'products/products_categories_partial.html', context)

    
	 
