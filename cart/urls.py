from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('add/', CartAddView.as_view(), name='cart_add'),
    path('remove/', CartRemoveView.as_view(), name='cart_remove'),
    path('delete/', CartDeleteView.as_view(), name='cart_delete'),
    path('', CartSummaryView.as_view(), name='cart'),
    
]
