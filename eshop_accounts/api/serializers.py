from products.models import Product
from rest_framework import exceptions, fields, serializers
from django.db import IntegrityError
from eshop_accounts.models import Suplier, User,Customer
from products.models import Product

import uuid, os
from django.core.mail import EmailMessage
from django.core.cache import cache

class SignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    
    class Meta:
        model = User
        fields = ['password1','password2','email','phone']
    
    def validate_password2(self,value):
        data = self.initial_data
        # print(self.initial_data)
        if data['password1'] != value:
            raise serializers.ValidationError('password not equal') 
        return data
      
        
    def save(self):
        try:       
            user = User.objects.create_user(email=self.validated_data['email'],phone=self.validated_data['phone'],password=self.validated_data['password1'])        
        except IntegrityError as e:
            raise e       
        return user


# customer
class SignupCustomerSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
)
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
)
    
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','password1','password2','phone','image']
    
    def validate_password2(self,value):
        data = self.initial_data        
        if data['password1'] != value:
            raise serializers.ValidationError('پسوردها برابر نیست!') 
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User.objects.create_user(password=password, **validated_data)
        Customer.objects.create(user=user)
        return user


class CustomerProfileViewSerializer(serializers.ModelSerializer): 
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','phone','image']


class UpdateCustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','image']

# suplier
class SignupSuplierSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
)
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
)
    bank_acconunt = serializers.CharField(write_only=True)   
    
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','password1','password2','phone','image', 'bank_acconunt']
    
    def validate_password2(self,value):
        data = self.initial_data        
        if data['password1'] != value:
            raise serializers.ValidationError('پسوردها برابر نیست!') 
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        bank = validated_data.pop('bank_acconunt')
        user = User.objects.create_user(password=password, **validated_data)
        self._send_mail(self.context['request'], user.email)
        Suplier.objects.create(user=user, bank_acconunt=bank)
        return user

    def _send_mail(self, request,user_email):
        TIMEOUT = 60 * 5 ## 5 minuites
        user_uuid = uuid.uuid4() 
        cache.set(user_uuid,user_email,TIMEOUT)
        msg = EmailMessage(
            'Signup via Email',
            f'click <a href="http://127.0.0.1:8000/eshop_accounts/email-verification/{user_uuid}/{user_email}/">Verify me</a> to be redirected to verifcation url :)<br><p>your email:{user_email}<br> your password :{user_uuid} <br> cahnge it after you logged in :) ',
            os.getenv('EMAIL_USERNAME'),
            [user_email,])
        
        # EmailMessage()
        msg.content_subtype = "html"  
        msg.send()
       


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def validate(self, attrs):
        if attrs['password1'] == attrs['password2']:
            return attrs
        else:
            raise serializers.ValidationError('Not equal')



class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name', 'last_name','phone','image']


class SuplierProfileViewSerializer(serializers.ModelSerializer):
    product_set = ProductListSerializer(many=True)
    class Meta:
        model = Suplier
        fields = ['user', 'product_set']

   


class SuplierCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['suplier','slug']

    def create(self, validated_data):
        sup = Suplier.objects.get(user=self.context['request'].user)
        product = Product.objects.create(suplier=sup, **validated_data)
        return product