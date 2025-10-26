"""Utility functions for orders app"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_order_confirmation_email(order):
    """Send order confirmation email to customer"""
    subject = f'Order Confirmation - {order.order_number}'
    
    html_message = render_to_string('orders/emails/order_confirmation.html', {
        'order': order,
        'items': order.items.all(),
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fruitshop.com',
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_order_status_update_email(order, old_status, new_status):
    """Send email when order status changes"""
    subject = f'Cập nhật trạng thái đơn hàng - {order.order_number}'
    
    # Get display name for status
    status_display = dict(order.STATUS_CHOICES).get(new_status, new_status)
    
    html_message = render_to_string('orders/emails/status_update.html', {
        'order': order,
        'old_status': old_status,
        'new_status': new_status,
        'new_status_display': status_display,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000',
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fruitshop.com',
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"[OK] Email sent successfully to {order.email}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email to {order.email}: {e}")
        return False


def send_delivery_assignment_email(delivery):
    """Send email to delivery person when assigned a delivery"""
    subject = f'Đơn Hàng Mới #{delivery.order.order_number} - Fresh Fruit Shop'
    
    # Get delivery person email
    delivery_person_email = delivery.delivery_person.user.email
    
    if not delivery_person_email:
        print(f"[ERROR] Delivery person {delivery.delivery_person.user.username} has no email address")
        return False
    
    html_message = render_to_string('orders/emails/delivery_assignment.html', {
        'delivery': delivery,
        'delivery_person': delivery.delivery_person,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000',
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fruitshop.com',
            recipient_list=[delivery_person_email],
            html_message=html_message,
            fail_silently=False,
        )
        print(f"[OK] Delivery assignment email sent successfully to {delivery_person_email}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send delivery assignment email to {delivery_person_email}: {e}")
        return False


def calculate_shipping_fee(total_amount):
    """Calculate shipping fee based on order total"""
    if total_amount >= 100:  # Free shipping for orders over $100
        return 0
    elif total_amount >= 50:
        return 5
    else:
        return 10


def validate_discount_code(code, user):
    """Validate discount code and return (is_valid, discount_object, message)"""
    from products.models import Discount
    
    try:
        discount = Discount.objects.get(code=code.upper())
        
        if not discount.is_valid:
            return False, None, "This discount code is not valid or has expired."
        
        # Return the discount object so we can check min_purchase later
        return True, discount, f"Discount code '{code}' applied successfully!"
        
    except Discount.DoesNotExist:
        return False, None, "Invalid discount code."


def get_cart_from_session(request):
    """Get cart data from session"""
    cart = request.session.get('cart', {})
    return cart


def add_to_cart(request, product_id, quantity=1):
    """Add product to cart session"""
    cart = get_cart_from_session(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        # Handle old format (int) by converting to new format (dict)
        if isinstance(cart[product_id_str], dict):
            cart[product_id_str]['quantity'] += quantity
        else:
            # Old format: convert to new format
            old_quantity = cart[product_id_str]
            cart[product_id_str] = {'quantity': old_quantity + quantity}
    else:
        cart[product_id_str] = {
            'quantity': quantity,
        }
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def update_cart(request, product_id, quantity):
    """Update cart item quantity"""
    cart = get_cart_from_session(request)
    product_id_str = str(product_id)
    
    if quantity > 0:
        if product_id_str in cart:
            # Handle old format by converting to new format
            if isinstance(cart[product_id_str], dict):
                cart[product_id_str]['quantity'] = quantity
            else:
                cart[product_id_str] = {'quantity': quantity}
    else:
        if product_id_str in cart:
            del cart[product_id_str]
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def remove_from_cart(request, product_id):
    """Remove product from cart"""
    cart = get_cart_from_session(request)
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
    
    request.session['cart'] = cart
    request.session.modified = True
    return cart


def clear_cart(request):
    """Clear entire cart"""
    request.session['cart'] = {}
    request.session.modified = True


def get_cart_items(request):
    """Get cart items with product details"""
    from products.models import Product
    
    cart = get_cart_from_session(request)
    items = []
    total = 0
    
    for product_id, item_data in cart.items():
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            
            # Handle both old format (int) and new format (dict)
            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
            else:
                # Old format: cart[product_id] = quantity (int)
                quantity = item_data
            
            price = product.get_price
            subtotal = price * quantity
            
            items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
            })
            total += subtotal
        except Product.DoesNotExist:
            # Remove invalid product from cart
            pass
    
    return items, total


def get_cart_count(request):
    """Get total number of items in cart"""
    cart = get_cart_from_session(request)
    count = 0
    for item in cart.values():
        if isinstance(item, dict):
            count += item.get('quantity', 0)
        else:
            # Old format: cart[product_id] = quantity (int)
            count += item
    return count

