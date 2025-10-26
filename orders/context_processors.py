"""
Context processors for orders app
"""
from .utils import get_cart_count


def cart_processor(request):
    """Add cart count to all templates"""
    return {
        'cart_count': get_cart_count(request)
    }


def wishlist_processor(request):
    """Add wishlist count to all templates"""
    if request.user.is_authenticated:
        from products.models import Wishlist
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    
    return {
        'wishlist_count': wishlist_count
    }