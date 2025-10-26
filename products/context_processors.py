"""
Context processors for products app
"""
from .models import Category


def categories_processor(request):
    """Add categories to all templates"""
    categories = Category.objects.filter(is_active=True).order_by('name')[:5]
    
    return {
        'footer_categories': categories
    }

