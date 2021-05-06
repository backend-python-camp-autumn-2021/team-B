from django.contrib import messages
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.urls import reverse_lazy
from .forms import LoginForm,RegisterForm
from django.contrib.auth import get_user_model
User = get_user_model()

class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            # logout(request)
            return redirect('/')
        form = LoginForm()
        next_url = request.GET.get('next', '')
        context = {
            'form': form,
            'next_url': next_url
        }
        return render(request, 'eshop_accounts/login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "کاربر عزیز خوش آمدید!")
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                return redirect('/')
            else:
                return redirect('login/')

class SignUp(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }

        return render(request, 'eshop_accounts/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            phone = register_form.cleaned_data['phone']
            try:
                User.objects.create_user(email=email, password=password, phone=phone)
                messages.success(request, "ثبت نام شما با موفقیت انجام شد!")
                
            except IntegrityError as e:

                messages.error(request, f"{e}")
                return redirect('login')

        context = {
            'register_form': register_form
        }
        return render(request, 'eshop_accounts/register.html', context)

# rest
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