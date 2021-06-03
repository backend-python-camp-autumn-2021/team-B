import django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import User,Suplier
from django.core import validators
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
User = get_user_model()

from eshop_accounts.models import Customer


# add user to group
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []
        

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(), 
         required=False,
         # Use the pretty 'filter_horizontal widget'.
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance

# 

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150,required=False, label='نام')
    last_name = forms.CharField(max_length=150,required=False, label='نام خانوادگی' )
    image = forms.ImageField(required=False, label='عکس' )

    class Meta:
        model = User
        fields = ("email","first_name","last_name","image")
        
 
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name')


# RegisterForm
class RegisterFormCustomer(CustomUserCreationForm):
    def save(self, *args,**kwrags):
        user = super().save(*args,**kwrags)
        customer = Customer.objects.create(user=user)
        return customer



class RegisterFormSuplier(CustomUserCreationForm):
    bankaccount = forms.CharField(max_length=30, label='حساب بانکی')

    def save(self, *args,**kwargs):        
        user = super().save(*args, **kwargs)
        permission = Permission.objects.get(codename='access_product')
        user.user_permissions.add(permission)
        sup = Suplier.objects.create(bank_acconunt=self.cleaned_data['bankaccount'], user=user)
        return sup


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خود را وارد نمایید', 'class': 'form-control'}),
        label='نام'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام خانوادگی خود را وارد نمایید', 'class': 'form-control'}),
        label='نام خانوادگی'
    )
    class Meta:
        model = User
        fields = ['first_name','last_name','image' ]
                  
        

