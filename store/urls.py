from django.urls import  path
from . import views


urlpatterns = [
    # store
    path('store/',views.store,name='store'),
    path('store/<slug:category_slug>/',views.store,name='products_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail') ,
    # cart
    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name='remove_cart_item'),
    # wishlist
   
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    path('search/',views.search,name='search'),
    path('remove_wishlist_item/<int:product_id>/',views.remove_wishlist_item,name='remove_wishlist_item'),
    # checkout
    path('cart/checkout/',views.checkout,name='checkout'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
]
