from django.contrib import admin
# Register your models here.
from .models import Product,Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active','Categories']
    prepopulated_fields = {'slug':('title',)}

    class Meta:
        model = Product



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title','slug']
    prepopulated_fields = {'slug':('title',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category,CategoryAdmin)
