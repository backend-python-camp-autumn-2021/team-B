# Generated by Django 3.2.2 on 2021-05-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('star_ratings', '0003_auto_20160721_1127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'امتیازدهی', 'verbose_name_plural': 'امتیازدهی'},
        ),
        migrations.AlterModelOptions(
            name='userrating',
            options={'verbose_name': 'امتیازدهی کاربر', 'verbose_name_plural': 'امتیازدهی کاربر'},
        ),
        migrations.AlterField(
            model_name='rating',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userrating',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]