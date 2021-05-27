from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.contrib.auth import get_user_model
User = get_user_model()


class AddToCartForm(forms.Form):
    count = forms.IntegerField(required=True,initial=1)
       