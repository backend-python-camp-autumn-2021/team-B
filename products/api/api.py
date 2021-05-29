from rest_framework import generics
from rest_framework.response import Response
# from rest_framework.views import APIView

from products.api.serializers import ProductSerializer
from products.models import Product, ProductsDetail


# class ProductListView(APIView):
#     def get(self, request):
#         products_qs = Product.objects.all()
#         serializer_data = ProductListSerializer(products_qs, many=True)
#         return Response(serializer_data.data)

# class ProductDetailApi(generics.RetrieveUpdateDestroyAPIView):
#     queryset = ProductsDetail.objects.all()
#     serializer_class = ProductDetailSerializer

class ProductApi(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
