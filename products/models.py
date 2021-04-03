from django.db import models
from users.models import Customer,Suplier,Address

# Create your models here.

class Categories(models.Model):
    name = models.CharField('نام دسته بندی',max_length=255)
    des = models.CharField('توضیح',null=True, blank=True,max_length=255)

class Subcategories(models.Model):
    name = models.CharField('نام',max_length=255)
    categories = models.ForeignKey(Categories, on_delete = models.CASCADE) 

class Products(models.Model):
    name = models.CharField(' نام محصول',max_length=255)   
    des = models.CharField('توضیح',null=True, blank=True,max_length=255) 
    image = models.ImageField('عکس', upload_to="Products_image/", null=True, blank=True)
    brand =models.CharField('نام برند', null=True, blank=True,max_length=255)
    price = models.FloatField('قیمت')
    quantitiy = models.IntegerField('مقدار')
    discount = models.IntegerField('تخفیف')
    subcategories = models.ForeignKey(Subcategories, on_delete = models.CASCADE)
    suplier = models.ForeignKey(Suplier, on_delete = models.CASCADE)    
   
class Products_detail():
    des = models.CharField(' جزییات',max_length=255)   
    products = models.ForeignKey(Products, on_delete = models.CASCADE)


class Feedback(models.Model):
    text = models.TextField('متن', null=True, blank=True)
    rate = models.FloatField(default=5)
    products = models.ForeignKey(Products, on_delete = models.CASCADE)

class Tag(models.Model):
    products = models.ForeignKey(Products, on_delete = models.CASCADE)


class Store(models.Model):
    address = models.CharField('آدرس',max_length=255)
    last_update = models.DateField()
    products = models.ForeignKey(Products, on_delete = models.CASCADE)


class Purchase(models.Model):
    ammount = models.IntegerField('مقدار')
    oreder_address = models.CharField('آدرس',max_length=255)
    shipping_address = models.CharField('آدرس حمل ونقل',max_length=255)
    order_date = models.DateTimeField()
    shopping_date = models.DateTimeField()
    CHOICE_CAT = [
        ('New', 'سفارش جدید'),
        ('Hold', 'تعلیق'),
        ('Shipped', 'درحال تحویل'),
        ('Deliverd', 'دریافت'),
        ('Closed', 'کنسل'),
    ]
    state = models.CharField(max_length=255, choices = CHOICE_CAT, unique=True)
    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)


class Cart(models.Model):
    des = models.CharField(max_length=255,  unique=True)
    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)

class line_item(models.Model):
    CHOICE_CAT = [
        ('buy', 'سفارش جدید'),
        ('Hold', 'تعلیق'),
        ]
    state = models.CharField(max_length=255, choices = CHOICE_CAT, unique=True) 
    quantity = models.IntegerField()
    price = models.IntegerField()
    products = models.ForeignKey(Products, on_delete = models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE)



class Payment(models.Model):
    pay_date = models.DateTimeField()
    total = models.IntegerField()
    details = models .TextField()
    cart = models.OneToOneField(Cart,on_delete = models.CASCADE)
    address = models.ForeignKey(Address, on_delete = models.CASCADE)