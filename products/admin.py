from django.contrib import admin


from .models import Product,Category



class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active','Categories']
    prepopulated_fields = {'slug':('title',)}

    class Meta:
        model = Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title','slug']
    prepopulated_fields = {'slug':('title',)}

# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category,CategoryAdmin)
admin.site.register(Product)
admin.site.register(Category)
