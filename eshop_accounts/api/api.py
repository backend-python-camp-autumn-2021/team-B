from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView
from .serializers import SignupSerializer,SignupCustomerSerializer,SignupSuplierSerializer,CustomerProfileViewSerializer,SuplierProfileViewSerializer,UpdateCustomerProfileSerializer,SuplierCreateProductSerializer

from django.core.cache import cache

from eshop_accounts.models import Customer, Suplier, User
from products.models import Product




class SignupCreate(CreateAPIView):
    serializer_class = SignupSerializer
    model = User
    
# logout
class LogoutApi(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# signup
class SignupCreateCustomer(CreateAPIView):
    serializer_class = SignupCustomerSerializer


class EmailVerifyApiView(APIView):
    def get(self, request, uuid, email):    
        _cached_email = cache.get(uuid)
        if _cached_email in email:
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
        return Response('ok  verify')


class SignupCreateSuplier(CreateAPIView):
    serializer_class = SignupSuplierSerializer


# profileview

class CustomerProfileView(RetrieveAPIView):
    serializer_class = CustomerProfileViewSerializer
    model = User

    def get_object(self):
        # print(self.request.user)
        return self.request.user

class SuplierProfileView(APIView):
    serializer_class = SuplierProfileViewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        suplier = Suplier.objects.get(user=request.user)
        serialized = self.serializer_class(suplier)
        return Response(serialized.data)

# update
class UpdateCustomerProfile(RetrieveUpdateAPIView):
    model = User
    serializer_class = UpdateCustomerProfileSerializer

    def get_object(self):        
        return self.request.user


# create
class SuplierCreateProduct(ListCreateAPIView):
    serializer_class = SuplierCreateProductSerializer

    def get_queryset(self):
        sup = Suplier.objects.get(user=self.request.user)
        query_set = Product.objects.filter(suplier=sup)
        return query_set
    
    # def get
