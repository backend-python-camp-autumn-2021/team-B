# Generated by Django 3.0.7 on 2021-05-15 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
                'db_table': 'auth_user',
            },
        ),
        migrations.CreateModel(
            name='Suplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_acconunt', models.CharField(max_length=255, unique=True, verbose_name='حساب بانکی')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'تامین کننده',
                'verbose_name_plural': 'تامین کنندگان',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='profile/', verbose_name='تصویر')),
                ('gender', models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], max_length=255, verbose_name='زن/مرد')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'مشتری',
                'verbose_name_plural': 'مشتریان',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='آدرس')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='شهر')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='کشور')),
                ('zipcode', models.IntegerField(blank=True, null=True, verbose_name='کدپستی')),
                ('fax', models.IntegerField(blank=True, null=True, verbose_name='فکس')),
                ('email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='ایمیل')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
    ]
