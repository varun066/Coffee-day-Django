from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import *

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'custom_id', 'price', 'description','image')
    search_fields = ('name', 'item_type', 'custom_id')
    list_filter = ('custom_id',)
    ordering = ('item_type', 'name')

    

class ItemInline(admin.TabularInline):
    model = Menu.items.through
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ItemInline]

admin.site.register(Item, ItemAdmin)
admin.site.register(Menu, MenuAdmin)

admin.site.register(Cart)
admin.site.register(CartItem)