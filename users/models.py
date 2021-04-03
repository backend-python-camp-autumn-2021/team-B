from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Address(models.Model):
    address = models.CharField('1 آدرس', null=True, blank=True,max_length=255)
    city = models.CharField('شهر',null=True,blank=True,max_length=255)
    country = models.CharField('کشور',null=True,blank=True,max_length=255)
    zipcode = models.IntegerField('کدپستی',null=True,blank=True)
    fax = models.IntegerField('فکس',null=True,blank=True)
    email = models.EmailField('ایمیل',max_length=255)
    phone = models.IntegerField('شماره تلفن')
    user= models. ForeignKey(User,on_delete = models.CASCADE)
             
class Customer(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [
        (GENDER_MALE, 'مرد'),
        (GENDER_FEMALE, 'زن'),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES)
    date_joined = models.DateTimeField()
    is_enabled = models.DateTimeField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.user= self.user.lower()
        return super().save(*args, **kwargs)

class Suplier(models.Model):
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField()
    bank_acconunt = models.CharField(max_length=255,unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.user= self.user.lower()
        return super().save(*args, **kwargs)

