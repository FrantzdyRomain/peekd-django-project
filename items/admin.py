from django.contrib import admin
from items.models import Item



class ItemAdmin(admin.ModelAdmin):
    list_display = ['owner']
    
admin.site.register(Item, ItemAdmin)
