"""
Template tags for products app
"""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def stars(rating):
    """Display star rating"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    html = '★' * full_stars
    if half_star:
        html += '☆'
    html += '☆' * empty_stars
    
    return mark_safe(f'<span class="stars" title="{rating:.1f}">{html}</span>')


@register.filter
def discount_percent(original_price, discounted_price):
    """Calculate discount percentage"""
    if original_price and discounted_price and original_price > discounted_price:
        percent = ((original_price - discounted_price) / original_price) * 100
        return f"{percent:.0f}%"
    return ""


@register.filter
def stock_status(stock):
    """Return stock status badge"""
    if stock > 10:
        return mark_safe('<span class="badge bg-success">In Stock</span>')
    elif stock > 0:
        return mark_safe(f'<span class="badge bg-warning">Only {stock} left</span>')
    else:
        return mark_safe('<span class="badge bg-danger">Out of Stock</span>')


@register.simple_tag
def price_range(products):
    """Get price range for products"""
    if not products:
        return "N/A"
    
    prices = [p.price for p in products]
    min_price = min(prices)
    max_price = max(prices)
    
    if min_price == max_price:
        return f"${min_price:,.0f}"
    return f"${min_price:,.0f} - ${max_price:,.0f}"


@register.filter
def vnd(value):
    """Format number as Vietnamese Dong"""
    try:
        value = float(value)
        # Format with thousand separators
        formatted = "{:,.0f}".format(value)
        # Replace comma with dot for Vietnamese format
        formatted = formatted.replace(',', '.')
        return f"{formatted}₫"
    except (ValueError, TypeError):
        return value
