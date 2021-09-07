from django.contrib import admin
from .models import *
# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre","precio"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["user"]

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["item"]

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
