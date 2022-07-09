from . import views
from django.urls import path

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments/',views.payments,name='payments'),
    path('payment_status/',views.payment_status,name='payment_status'),
    path('payment_success/',views.payment_success,name='payment_success'),
    path('payment_failed/',views.payment_failed,name='payment_failed'),
]