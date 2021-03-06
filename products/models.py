from django.db import models
from django.contrib.auth.models import Permission, User
from django.db import models
from django.db.models.fields import SlugField
from eshop_accounts.models import Customer, Suplier, Address,User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255,verbose_name='عنوان')
    is_sub = models.BooleanField(default=False,null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=True,verbose_name='عنوان در URL')
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True, related_name='child',
                               related_query_name='child')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title



class Product(models.Model):
    title = models.CharField(max_length=255,verbose_name='عنوان')
    description = models.TextField(max_length=255, null=True, blank=True,verbose_name='توضیحات')
    slug = models.SlugField(max_length=200, unique=True,allow_unicode=True,verbose_name='عنوان در URL')
    image = models.ImageField(upload_to="Products_image/", null=True, blank=True,verbose_name='تصویر')
    brand = models.CharField(null=True, blank=True, max_length=255,verbose_name='برند')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=0,verbose_name='قیمت')
    active = models.BooleanField(default=True,verbose_name='فعال / غیرفعال')
    created = models.DateTimeField(auto_now_add=True,verbose_name='زمان ساخت ')
    updated = models.DateTimeField(auto_now=True,verbose_name='به روزرسانی ')
    discount = models.FloatField(null=True, blank=True,verbose_name='تخفیف')
    comments = GenericRelation(Comment)
    visit_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    Categories = models.ForeignKey(Category, on_delete=models.PROTECT, null=True,verbose_name='دسته بندی ها')
    # category = models.ManyToManyField(Category, related_name='products')
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE,verbose_name='تامین کننده')

 
    class Meta:
        permissions = [('access_product','access to CRUD of product')]
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title[:20])
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        pass

		
class ProductsDetail(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    caption = models.TextField(max_length=5000, blank=True)
    products = models.OneToOneField(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    text = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    rate = models.FloatField(default=5)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    slug = models.SlugField(verbose_name='عنوان در url')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    products = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, verbose_name='محصولات')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب / تگ'
        verbose_name_plural = 'برچسب ها / تگ ها'



class Store(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=255)
    about = models.TextField(max_length=2000, blank=True)
    last_update = models.DateField()
    owners = models.ManyToManyField(Suplier)
    Address = models.ForeignKey(Address, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Cart(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'open'),
        ('CLOSED', 'closed')
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.IntegerField(blank=True, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'

    def __str__(self):
        return self.user.phone
    
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return int( total - discount_price )
        return total


class CartItem(models.Model):
    quantity = models.IntegerField(default=0)
    # price = models.IntegerField(verbose_name='قیمت محصول')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', related_query_name='cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', related_query_name='item')

    class Meta:
        verbose_name = 'جزییات محصول'
        verbose_name_plural = 'اطلاعات جزییات محصولات'

    def __str__(self):
        return self.products.title

    def get_cost(self):
        return self.products.price * self.quantity
    


class Payment(models.Model):
    pay_date = models.DateField()
    total = models.FloatField()
    details = models.TextField(max_length=255, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.details
