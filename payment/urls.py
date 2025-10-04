from django.urls import path
from .views import *


app_name = 'payment'
urlpatterns = [
    path('process-order', ProcessOrderView.as_view(), name='process_order'),
    path('chechout/', CheckoutView.as_view(), name='checkout'),
    path('shiping-form/', ShippingView.as_view(), name='shiping_form'),
    path('final-check/', FinalCheckView.as_view(), name='final_check'),
    path('order-detail/<slug:slug>/', OrderDetailView.as_view(), name='order_detail')
]
