from django.contrib import admin
from .models import ShipingAddress, Order, OrderItem

admin.site.register(ShipingAddress)

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_ordered', 'update')
    inlines = (OrderItemInline,)
