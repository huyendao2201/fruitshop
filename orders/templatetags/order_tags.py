"""
Template tags for orders app
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def order_status_badge(status):
    """Display order status badge"""
    badges = {
        'pending': '<span class="badge bg-warning">Pending</span>',
        'processing': '<span class="badge bg-info">Processing</span>',
        'shipped': '<span class="badge bg-primary">Shipped</span>',
        'delivered': '<span class="badge bg-success">Delivered</span>',
        'cancelled': '<span class="badge bg-danger">Cancelled</span>',
        'refunded': '<span class="badge bg-secondary">Refunded</span>',
    }
    return mark_safe(badges.get(status, status))


@register.filter
def payment_method_icon(method):
    """Display payment method icon"""
    icons = {
        'cash': '💵',
        'card': '💳',
        'momo': '📱',
        'bank': '🏦',
    }
    return icons.get(method, '💰')


@register.filter
def multiply(value, arg):
    """Multiply filter for templates"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def currency(value):
    """Format as currency"""
    try:
        return f"{float(value):,.0f}đ"
    except (ValueError, TypeError):
        return "0đ"

