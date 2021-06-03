from django.urls import path
from . import views


app_name = 'contact'
urlpatterns = [
    path('contact-us', views.ContactPage.as_view(), name='contact_us'),
   

]