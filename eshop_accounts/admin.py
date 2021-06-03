from django.contrib import admin
from django.contrib import messages
from .models import  Customer, Suplier, Address
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, GroupAdminForm
from django.contrib.auth.models import Group
from .models import User



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active','is_superuser','phone',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('اطلاعات اصلی', {'fields': ('email', 'password', 'first_name')}),
        ('Permissions', {
         'fields': ('is_staff', 'is_active', 'user_permissions','is_superuser','groups',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'user_permissions', 'phone',)}
         ),
    )
    search_fields = ('is_staff',)
    ordering = ('email',)


# custom group
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']
   

# group = Group.objects.get(name='دسترسی ساپلایر')
# user.groups.add(group)


admin.site.register(User)
admin.site.register(Address)
admin.site.register(Customer)
admin.site.register(Suplier)
# gruop
#unRegister basic  Group
admin.site.unregister(Group)
# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)








