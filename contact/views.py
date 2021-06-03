from django.shortcuts import render
from django.views.generic import  CreateView
from .models import ContactUs,SiteSetting
from django.urls import reverse_lazy

# Create your views here.
from .forms import CreateContactForm


class ContactPage(CreateView):
    model = ContactUs
    form_class = CreateContactForm
    template_name = 'contact/contact_us_page.html'
    success_url = reverse_lazy('contact:contact_us')
    
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['contact_form'] = CreateContactForm()
        context['setting'] = SiteSetting.objects.first()
        return context

