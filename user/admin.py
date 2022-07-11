from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import user

# Register your models here.

class userAdmin(UserAdmin):
    list_display = ('id','email','first_name','last_name','username','last_login','is_active','date_joined')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(user,userAdmin)
