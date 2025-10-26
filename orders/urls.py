from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Cart management
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-to-cart/<int:product_id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-cart/<int:product_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('clear-cart/', views.ClearCartView.as_view(), name='clear_cart'),
    
    # Checkout
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('apply-discount/', views.ApplyDiscountView.as_view(), name='apply_discount'),
    path('remove-discount/', views.RemoveDiscountView.as_view(), name='remove_discount'),
    
    # Orders
    path('my-orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<str:order_number>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
    
    # VNPay payment
    path('vnpay/payment/<int:order_id>/', views.VNPayPaymentView.as_view(), name='vnpay_payment'),
    path('vnpay/return/', views.VNPayReturnView.as_view(), name='vnpay_return'),
    path('vnpay/ipn/', views.VNPayIPNView.as_view(), name='vnpay_ipn'),
]