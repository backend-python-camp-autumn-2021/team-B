from django.urls import path
# from products.api.api import ProductApi
from products import views
from products.api.api import ProductApi



app_name = 'products'
urlpatterns = [
    # router.urls,
    path('api', ProductApi.as_view()),
    path('products', views.ProductsList.as_view(), name='product-list'),
    path('products/search', views.SearchProductsView.as_view(), name='product-serach'),
    path('category/<Category_title>', views.ProductsListByCategory.as_view(), name='product-cat'),
    path('products/<int:pk>/', views.ProductsDetail.as_view(), name='product-detail'),
    path('products_categories_partial', views.products_categories_partial, name='products_categories_partial'),
]
