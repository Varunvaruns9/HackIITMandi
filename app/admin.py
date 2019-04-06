from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'first_name', 'last_name', 'is_staff', 'donor', 'organs', 'bloodgroup', 'rh', 'ailment', 'report')