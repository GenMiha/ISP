from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Item


# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
