from django.contrib import admin
from .models import Order, OrderItem

class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
    ('Product',{'fields':['product'],}),
    ('Quantity',{'fields':['quantity'],}),
    ('Price',{'fields':['price'],}),
    ]
    readonly_fields = ['product','quantity','price']
    can_delete = False
    max_num = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','billingName','emailAddress','created']
    list_display_links = ('id','billingName')
    search_fields = ['id','billingName','emailAddress']
    readonly_fields = ['id','token','total','emailAddress','created','billingName','shippingName','shippingAddress1','shippingCity','shippingCountry']
    fieldsets = [
    ('ORDER INFORMATION',{'fields': ['id','token','total','created']}),
    ('BILLING INFORMATION', {'fields': ['billingName','emailAddress']}),
    ('SHIPPING INFORMATION', {'fields': ['shippingName','shippingAddress1','shippingCity','shippingCountry']}),
    ]

    inlines = [
        OrderItemAdmin
    ]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


admin.site.register(Order, OrderAdmin)
