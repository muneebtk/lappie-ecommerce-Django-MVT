from . import views
from django.urls import path

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('home/',views.home ,name='home'),

    # path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotpassword/',views.forgotpassword ,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword ,name='resetpassword'),
    path('verify/',views.verify_code,name ='verify_code'),
     
    path('account/',views.account,name='account'),
    path('edit_account/<int:id>/',views.edit_account,name='edit_account'),
    path('orders/',views.orders,name='orders'),
]
