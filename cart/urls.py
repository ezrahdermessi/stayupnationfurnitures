from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment/initiate/', views.initiate_payment, name='initiate_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/manual/', views.manual_order_create, name='manual_order_create'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
]