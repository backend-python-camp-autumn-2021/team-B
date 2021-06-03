
import redis
import secrets
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView,RetrieveAPIView,RetrieveUpdateDestroyAPIView,UpdateAPIView
from .serializers import (
    SignupSerializer,SignupCustomerSerializer,SignupSuplierSerializer,
    CustomerProfileViewSerializer,SuplierProfileViewSerializer,
    UpdateCustomerProfileSerializer,SuplierCreateProductSerializer,
    ResetPasswordSerializer,SetPasswordSerializer)

from django.core.cache import cache

from eshop_accounts.models import Customer, Suplier, User
from products.models import Product


class SignupCreate(CreateAPIView):
    serializer_class = SignupSerializer


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
# rest
class ResetPasswordApiView(APIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serilizered_data = self.serializer_class(data=request.data)
        if serilizered_data.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            token = secrets.token_urlsafe(16)
            email = serilizered_data.data['email']
            r.set(token, email, ex=60*40)
            message = f'for resetting your password send your new \
                 and confirm password with post method to \
                <a href="http://localhost:8000/user/set_password_api/{token}/">here</a>'

            send_mail(
                'ResetPassword',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            r.close()
        return Response("Go and Check your email")

class SetPasswordApiView(APIView):
    serializer_class = SetPasswordSerializer

    def post(self, request, token):
        serilized_data = self.serializer_class(data=request.data)
        if serilized_data.is_valid():
            r = redis.Redis(host='localhost', port=6379, db=0)
            print(type(r.get(token)))
            mail = r.get(token).decode('utf-8')
            print(mail)
            user = User.objects.get(email=mail)
            print(serilized_data.validated_data['password1'])
            user.set_password(serilized_data.validated_data['password1'])
            user.save()
            return Response(serilized_data.validated_data, status=status.HTTP_200_OK)
        
        return Response(serilized_data.errors, status=status.HTTP_400_BAD_REQUEST)