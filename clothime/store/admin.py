from django.contrib import admin
from . models import Cart, CartItem, Coupons, FeaturedProduct, Product, Variation, Wishlist,HomeCarousel,CouponUser

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user','product','cart','quantity','is_active')
    
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id','user','product')

class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('id','product')

class HomeCouroselAdmin(admin.ModelAdmin):
    list_display = ('image','main_text','sub_text')

class CouponsAdmin(admin.ModelAdmin):
    list_display=('coupon_name','limit','discount_amount')

class CoupenUserAdmin(admin.ModelAdmin):
    list_display = ['cur_user','coupon']

admin.site.register(Product,ProductAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(FeaturedProduct,FeaturedProductAdmin)
admin.site.register(HomeCarousel,HomeCouroselAdmin)
admin.site.register(Coupons,CouponsAdmin)
admin.site.register(CouponUser,CoupenUserAdmin)

