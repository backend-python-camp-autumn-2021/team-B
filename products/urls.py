from django.db import router
from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from .api import api
router = SimpleRouter()
router.register(r'products-api',api.ProductViewSet,basename='products-api')
app_name = 'products'
urlpatterns = [
	
    path('products',views.ProductsList.as_view(),name='product-list'),
    path('products/search', views.SearchProductsView.as_view(),name='product-serach'),
    path('category/<Category_title>', views.ProductsListByCategory.as_view(),name='product-cat'),
    path('products/<int:pk>/',views.ProductsDetail.as_view(),name='product-detail'),
    path('products_categories_partial',views.products_categories_partial, name='products_categories_partial'),
    # api
    path('products-list-api',api.ProductList.as_view(), name='products_list_api'),
    path('products-detail-api/<int:pk>/',api.ProductDetail.as_view(), name='products_detail_api'),
    path('create-category-api/',api.CreateCategoryApiView.as_view(), name='create_category_api'),
]+router.urls
