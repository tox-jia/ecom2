from django.contrib import admin
from .models import ShippingAddress, Order, OrderItems
from django.contrib.auth.models import User

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItems)

# create an OderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItems
    extra = 0

# extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    # showing what is hidden:
    readonly_fields = ['date_ordered']
    # another way of showing what you want:
    fields = ['user', 'full_name', 'email',
              'shipping_address', 'amount_paid',
              'date_ordered', 'shipped', 'date_shipped',
              'invoice', 'paid']
    inlines = [OrderItemInline]

# Unregister Order Model
admin.site.unregister(Order)

# re-register our order and orderitem
admin.site.register(Order, OrderAdmin)

