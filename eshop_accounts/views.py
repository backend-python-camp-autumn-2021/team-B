from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect, reverse,get_object_or_404
from django.contrib.auth import views as auth_views
from django.views import View
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from django.urls import reverse_lazy
from .forms import LoginForm,RegisterForm,EditUserForm
from django.contrib.auth import get_user_model
User = get_user_model()

class UserLogin(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        form = LoginForm()
        next_url = request.META['HTTP_REFERER']
        print(next_url)
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
                return redirect(reverse_lazy('eshop_accounts:login'))

class SignUp(View):
    def get(self, request):
        register_form = RegisterForm()
        next_url = request.META['HTTP_REFERER']
        context = {
            'register_form': register_form,
            'next_url': next_url
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
                next_url = request.GET.get('next_url')
                if next_url:
                    return redirect(next_url)
                return redirect('/')
                
            except IntegrityError as e:

                messages.error(request, "لطفا دوباره ثبت نام کنید")
                return redirect(reverse_lazy('eshop_accounts:signup'))

        context = {
            'register_form': register_form
        }
        return render(request, 'eshop_accounts/register.html', context)


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





@login_required
def user_account_main_page(request):
    return render(request, 'eshop_accounts/user_account_main.html', {})


@login_required
def edit_user_profile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    edit_user_form = EditUserForm(request.POST or None,
                                  initial={'first_name': user.first_name, 'last_name': user.last_name})

    if edit_user_form.is_valid():
        first_name = edit_user_form.cleaned_data.get('first_name')
        last_name = edit_user_form.cleaned_data.get('last_name')

        user.first_name = first_name
        user.last_name = last_name
        user.save()

    context = {'edit_form': edit_user_form}

    return render(request, 'eshop_accounts/edit_account.html', context)


def user_sidebar(request):
    return render(request, 'eshop_accounts/user_sidebar.html', {})
