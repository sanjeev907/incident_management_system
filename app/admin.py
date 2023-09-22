from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class CustomeUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email','phone_number','state','country','fax','pincode','address','city']
    fieldsets = UserAdmin.fieldsets  + (
        ('Custom Fields', {'fields':('phone_number','state','country','fax','pincode','address','city',)}),
    )


admin.site.register(User,CustomeUserAdmin)