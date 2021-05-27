import uuid
import os

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import request
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import views as auth_views
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.core.mail import EmailMessage

from eshop_accounts.models import Customer, Suplier
from products.forms import CreateProductForm
from .forms import RegisterFormSuplier, UserCreationForm, RegisterFormCustomer,EditUserForm
from products.models import Product

User = get_user_model()


# login
class UserLogin(LoginView):
    template_name = 'eshop_accounts/login.html'

    def get_success_url(self):
        return '/'

# Customer   
class SignUpCustomer(auth_views.FormView):
    template_name="eshop_accounts/register.html"
    form_class = RegisterFormCustomer

    def get_success_url(self):
        return reverse_lazy('eshop_accounts:login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


class CustomerProfileView(View):  
    def get(self, request):
        user= User.objects.get(pk=request.user.pk)
        return render(request,'eshop_accounts/user_account_main.html',{"user":user})   


class UpdateCustomerView(UpdateView):
    form_class = EditUserForm
    model = User
    template_name = 'eshop_accounts\edit_account.html'
   

    def get_success_url(self):
        url = reverse_lazy('eshop_accounts:edit', args=[self.request.user.pk])
        return url

   
# sidebar profile
def user_sidebar(request):
    return render(request, 'eshop_accounts/user_sidebar.html', {})

# Suplier
class SignUpSuplier(auth_views.FormView):
    template_name="eshop_accounts/register2.html"
    form_class = RegisterFormSuplier

    def get_success_url(self):
        return reverse_lazy('eshop_accounts:login')

    def form_valid(self, form):
        user = form.save()
        self.send_mail(request, user.user.email)
        return super().form_valid(form)

    def send_mail(self, request,user_email):
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


def verify(request,user_uuid,user_email):
    _cached_email = cache.get(user_uuid)
    if _cached_email in user_email:
        user = User.objects.get(email = user_email)
        user.is_active = True
        user.save()
    return redirect("/")


class CreateProductView(CreateView):
    form_class = CreateProductForm
    model = Product
    template_name = 'eshop_accounts\create_account.html'

    def get_success_url(self):
        url = reverse_lazy('eshop_accounts:supplier_profile')
        return url

    def form_valid(self, form):
        suplier = Suplier.objects.get(user=self.request.user)
        form.instance.suplier = suplier
        return super().form_valid(form)


class SuplierProfileView(PermissionRequiredMixin, View):   
    permission_required = 'products.access_product'

    def get(self, request):
        suplier = Suplier.objects.get(user=request.user)
        products = Product.objects.filter(suplier=suplier, active=True)
        return render(request, 'eshop_accounts\suplier_account.html', {'suplier': suplier, 'products': products})


def log_out(request):
    logout(request)
    return redirect('/')
    

# reset
class UserPassReset(auth_views.PasswordResetView):
	template_name = 'eshop_accounts/password_reset_form.html'
	success_url = reverse_lazy('eshop_accounts:password_reset_done')
	email_template_name = 'eshop_accounts/password_reset_email.html'


class PasswordResetDone(auth_views.PasswordResetDoneView):
	template_name = 'eshop_accounts/reset_done.html'


class PasswordResetConfirm(auth_views.PasswordResetConfirmView):
	template_name = 'eshop_accounts/password_reset_confirm.html'
	success_url = reverse_lazy('eshop_accounts:password_reset_complete')


class PasswordResetComplete(auth_views.PasswordResetCompleteView):
	template_name = 'eshop_accounts/password_reset_complete.html'
