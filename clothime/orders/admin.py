from django.contrib import admin
from . models import Payment,Order,OrderProduct,Address

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','user','payment','address','order_total','tax','status','is_ordered','created_at','updated_at']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','status']
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id','user','payment_id','amount_paid','paid','order_id']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id','user']

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['quantity','payment','user','product']


admin.site.register(Payment,PaymentAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
admin.site.register(Address,AddressAdmin)

