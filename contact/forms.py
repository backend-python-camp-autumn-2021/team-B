from django.forms import ModelForm,TextInput,EmailInput,Textarea
from django.core import validators
from .models import ContactUs

class CreateContactForm(ModelForm):
    
    class Meta:
        model = ContactUs
        fields = ('full_name', 'email', 'subject','text')
        labels = {
            'full_name':'نام  ونام خانوادگی ',
            'email':'ایمیل',
            'subject':'عنوان',
            'text':'متن پیام',
        }
        widgets = {
            'full_name': TextInput(attrs={'placeholder': 'لطفا نام و نام خانوادگی خود را وارد نمایید', 'class': 'form-control'}),
            'email': EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
            'subject': TextInput(attrs={'placeholder': 'لطفا عنوان خود را وارد نمایید', 'class': 'form-control'}),
            'text': Textarea(attrs={'placeholder': 'لطفا متن پیام خود را وارد نمایید', 'class': 'form-control', 'rows': '8',
                   'cols': '20'}),
        }

        error_messages = {
            'full_name': {
                'max_length': (150, 'نام و نام خانوادگی شما نمیتواند بیشتر از 150 کاراکتر باشد'),
            },
            'email': {
                'max_length': (100, 'ایمیل شما نمیتواند بیشتر از 100 کاراکتر باشد'),
            },
            'subject': {
                'max_length':(200, 'عنوان پیام شما نمیتواند بیشتر از 200 کاراکتر باشد'),
            },
            
        }

    # def save(self, *args, **kwargs):
    #     full_name = self.cleaned_data.get('full_name')
    #     email = self.cleaned_data.get('email')
    #     subject = self.cleaned_data.get('subject')
    #     text = self.cleaned_data.get('text')
    #     ContactUs.objects.create(full_name=full_name, email=email, subject=subject, text=text, is_read=False)
    #     # todo : show user a success message
        

       