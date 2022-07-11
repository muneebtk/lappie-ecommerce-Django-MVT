from . import views
from django.urls import path

urlpatterns = [
    path('',views.admin_panel,name='admin_panel'),
    path('a_home/',views.a_home,name='a_home'),
    path('a_orders/',views.a_orders,name='a_orders'),
    path('a_users/',views.a_users,name='a_users'),
    path('a_products/',views.a_products,name='a_products'),
    path('a_category/',views.a_category,name='a_category'),
    path('a_featured_product/',views.a_featured_product,name='a_featured_product'),
    path('a_variation/',views.a_variation,name='a_variation'),
   
    path('a_payment/',views.a_payment,name='a_payment'),
    path('a_order_product/',views.a_order_product,name='a_order_product'),
    path('a_block_user/<int:id>/',views.a_block_user,name='a_block_user'),
    path('a_unblock_user/<int:id>/' ,views.a_unblock_user,name='a_unblock_user'),
    path('a_add_product/' ,views.a_add_product,name='a_add_product'),
    path('a_delete_product/<int:id>/' ,views.a_delete_product,name='a_delete_product'),
    path('a_edit_product/<int:id>/' ,views.a_edit_product,name='a_edit_product'),
    path('a_add_category/' ,views.a_add_category,name='a_add_category'),
    path('a_edit_category/<int:id>/' ,views.a_edit_category,name='a_edit_category'),
    path('a_delete_category/<int:id>/' ,views.a_delete_category,name='a_delete_category'),
    path('a_profile/',views.a_profile,name='a_profile'),
    path('a_delete_variation/<int:id>/',views.a_delete_variation,name='a_delete_variation'),
    path('a_add_variation/',views.a_add_variation,name='a_add_variation'),
    path('a_edit_variation/<int:id>/',views.a_edit_variation,name='a_edit_variation'),
    path('a_logout/',views.a_logout,name='a_logout'),

    path('a_view_order/<int:id>/',views.a_view_order,name='a_view_order'),
    path('a_category_search/',views.a_category_search,name='a_category_search'),
    path('a_add_featured_product/',views.a_add_featured_product,name='a_add_featured_product'),
    path('a_delete_featured_product/<int:id>/',views.a_delete_featured_product,name='a_delete_featured_product'),
    path('a_user_search/',views.a_user_search,name='a_user_search'),
    path('a_home_carousel/',views.a_home_carousel,name='a_home_carousel'),
    path('a_coupons/',views.a_coupons,name='a_coupons'),
    path('a_add_coupon/',views.a_add_coupon,name='a_add_coupon'),
    path('a_delete_coupon/<int:id>/',views.a_delete_coupon,name='a_delete_coupon'),
    path('a_home_carousel/',views.a_home_carousel,name='a_home_courosel'),
    path('a_edit_home_carousel/<int:id>/',views.a_edit_home_carousel,name='a_edit_home_carousel'),
    path('a_delete_home_carousel/<int:id>/',views.a_delete_home_carousel,name='a_delete_home_carousel'),
    path('a_add_home_carousel/',views.a_add_home_carousel,name='a_add_home_carousel'),
    path('a_order_search/',views.a_order_search,name='a_order_search'),
    path('a_product_search/',views.a_product_search,name='a_product_search'),
    path('a_variation_search/',views.a_variation_search,name='a_variation_search'),


]