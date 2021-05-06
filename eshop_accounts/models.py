from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, phone, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, phone,  **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password,phone, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True,verbose_name='ایمیل')
    phone = models.CharField(max_length=11,null=True,blank=True,verbose_name='شماره تلفن')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']
    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, related_name='profile',verbose_name='کاربر')
    image = models.ImageField(upload_to='profile/', null=True,verbose_name='تصویر')
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        
    ]
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES,verbose_name='زن/مرد')
    birth_date = models.DateField(null=True, blank=True,verbose_name='تاریخ تولد')

    class Meta:
      
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'
    
    def __str__(self):
        return self.user.email

    def number_address(self):
        return len(self.address.all())

    def save(self, *args, **kwargs):
        # if not self.phone:
        #     raise ValueError("please enter your phone number")
        if not self.user:
            user_obj = User.objects.create(username=self.phone)
            self.user = user_obj
        return super(Profile, self).save(*args, **kwargs)


class Address(models.Model):
    address = models.CharField(null=True, blank=True, max_length=255,verbose_name='آدرس')
    city = models.CharField(null=True, blank=True, max_length=255,verbose_name='شهر')
    country = models.CharField(null=True, blank=True, max_length=255,verbose_name='کشور')
    zipcode = models.IntegerField( null=True, blank=True,verbose_name='کدپستی')
    fax = models.IntegerField(null=True, blank=True,verbose_name='فکس')
    email = models.EmailField(max_length=255, null=True, blank=True,verbose_name='ایمیل')
    phone = models.CharField(max_length=11,null=True, blank=True,verbose_name='شماره تلفن' )
    # ForeignKey
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='کاربر')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

class Customer(models.Model):
    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='کاربر')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    # def save(self, *args, **kwargs):
    #     self.user = self.user.lower()
    #     return super().save(*args, **kwargs)


class Suplier(models.Model):
    
    bank_acconunt = models.CharField(max_length=255, unique=True,verbose_name='حساب بانکی')
    # OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name='کاربر')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'تامین کننده'
        verbose_name_plural = 'تامین کنندگان'

    # def save(self, *args, **kwargs):
    #     self.user = self.user.lower()
    #     return super().save(*args, **kwargs)
