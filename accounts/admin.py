from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'score', 'rank')
    
CustomUserAdmin.fieldsets[1][1]["fields"] += "score", "rank"

admin.site.register(User, CustomUserAdmin)