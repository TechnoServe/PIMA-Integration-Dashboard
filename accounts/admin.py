from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm
# Register your models here.



class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    
    # model = User
    ordering = ('email',)
    
    list_display = [
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_superuser"
    ]

    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        # ('Groups', {'fields': ('groups',)}),
        # ('Permissions', {'fields': ('user_permissions',)}),
    )

    list_filter = ('is_superuser',)

    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, CustomUserAdmin)