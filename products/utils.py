"""Các hàm tiện ích cho app products"""
from django.db.models import Q


def search_products(query, category=None, min_price=None, max_price=None, in_stock=False, sort_by=None):
    """
    Tìm kiếm sản phẩm nâng cao với các bộ lọc
    """
    from .models import Product
    
    products = Product.objects.filter(is_active=True)
    
    # Tìm kiếm theo văn bản
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(meta_keywords__icontains=query)
        )
    
    # Lọc theo danh mục
    if category:
        products = products.filter(category=category)
    
    # Lọc theo khoảng giá
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)
    
    # Lọc theo tồn kho
    if in_stock:
        products = products.filter(stock__gt=0)
    
    # Sắp xếp
    if sort_by:
        products = products.order_by(sort_by)
    
    return products


def get_featured_products(limit=8):
    """Lấy các sản phẩm nổi bật cho trang chủ"""
    from .models import Product
    return Product.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:limit]


def get_new_products(limit=8):
    """Lấy các sản phẩm mới nhất"""
    from .models import Product
    return Product.objects.filter(is_active=True, is_new=True).order_by('-created_at')[:limit]


def get_bestsellers(limit=8):
    """Lấy các sản phẩm bán chạy nhất"""
    from .models import Product
    return Product.objects.filter(is_active=True, is_bestseller=True).order_by('-created_at')[:limit]


def get_related_products(product, limit=4):
    """Lấy các sản phẩm liên quan từ cùng danh mục"""
    from .models import Product
    return Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id).order_by('?')[:limit]

