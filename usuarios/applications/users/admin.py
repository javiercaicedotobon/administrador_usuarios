from django.contrib import admin
from .models import User
# Register your models here.



class UserAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'username',
        'get_full_name',
        'email',
        'genero',
        'is_staff',
        'is_superuser',
        'is_active',
        'codregistro',        
    )



admin.site.register(User, UserAdmin)