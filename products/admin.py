from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage, Review, Wishlist, ShopReview, Newsletter


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Quản trị danh mục sản phẩm"""
    list_display = ('name', 'product_count', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')


class ProductImageInline(admin.TabularInline):
    """Inline để quản lý hình ảnh sản phẩm"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')


class ReviewInline(admin.TabularInline):
    """Inline để quản lý đánh giá sản phẩm"""
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'title', 'comment', 'created_at')
    can_delete = True
    fields = ('user', 'rating', 'title', 'is_approved', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Quản trị sản phẩm"""
    list_display = ('name', 'category', 'display_price', 'stock', 'stock_status_badge', 
                    'average_rating', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_new', 'is_bestseller', 'created_at')
    search_fields = ('name', 'description', 'short_description', 'meta_keywords')
    list_editable = ('stock', 'is_featured', 'is_active')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'average_rating', 'review_count')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ReviewInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description')
        }),
        ('Giá & Tồn kho', {
            'fields': ('price', 'discount_price', 'stock', 'unit')
        }),
        ('Chi tiết sản phẩm', {
            'fields': ('origin', 'nutrition_info')
        }),
        ('Trạng thái & Tính năng', {
            'fields': ('is_active', 'is_featured', 'is_new', 'is_bestseller')
        }),
        ('Hình ảnh', {
            'fields': ('image',)
        }),
        ('SEO', {
            'fields': ('meta_keywords', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Thống kê', {
            'fields': ('average_rating', 'review_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_price(self, obj):
        """Hiển thị giá với định dạng đặc biệt cho giá khuyến mãi"""
        if obj.discount_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">${}</span> <span style="color: #28a745; font-weight: bold;">${}</span>',
                obj.price, obj.discount_price
            )
        return f"${obj.price}"
    display_price.short_description = 'Giá'

    def stock_status_badge(self, obj):
        """Hiển thị trạng thái tồn kho với màu sắc"""
        if obj.stock == 0:
            color = 'red'
        elif obj.stock < 10:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.stock_status
        )
    stock_status_badge.short_description = 'Trạng thái kho'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Quản trị hình ảnh sản phẩm"""
    list_display = ('product', 'image_thumbnail', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'order')

    def image_thumbnail(self, obj):
        """Hiển thị thumbnail hình ảnh"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return '-'
    image_thumbnail.short_description = 'Hình thu nhỏ'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Quản trị đánh giá sản phẩm"""
    list_display = ('user', 'product', 'rating_stars', 'title', 'is_verified_purchase', 
                    'is_approved', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'created_at')
    search_fields = ('user__username', 'product__name', 'title', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at')

    def rating_stars(self, obj):
        """Hiển thị đánh giá bằng ngôi sao"""
        stars = '⭐' * obj.rating
        return stars
    rating_stars.short_description = 'Đánh giá'


@admin.register(ShopReview)
class ShopReviewAdmin(admin.ModelAdmin):
    """Quản trị đánh giá cửa hàng"""
    list_display = ('user', 'rating_stars', 'title', 'is_verified_purchase', 
                    'is_approved', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'is_approved', 'is_featured', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'comment')
    list_editable = ('is_approved', 'is_featured')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin đánh giá', {
            'fields': ('user', 'rating', 'title', 'comment')
        }),
        ('Trạng thái', {
            'fields': ('is_verified_purchase', 'is_approved', 'is_featured')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def rating_stars(self, obj):
        """Hiển thị đánh giá bằng ngôi sao"""
        stars = '⭐' * obj.rating
        return stars
    rating_stars.short_description = 'Đánh giá'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Quản trị danh sách yêu thích"""
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    """Quản trị đăng ký nhận tin"""
    list_display = ('email', 'status_badge', 'subscribed_at', 'unsubscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at', 'unsubscribed_at')
    date_hierarchy = 'subscribed_at'
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    fieldsets = (
        ('Thông tin đăng ký', {
            'fields': ('email', 'is_active')
        }),
        ('Thời gian', {
            'fields': ('subscribed_at', 'unsubscribed_at')
        }),
    )
    
    def status_badge(self, obj):
        """Hiển thị trạng thái với màu sắc"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Đang hoạt động</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">✗ Đã hủy</span>'
        )
    status_badge.short_description = 'Trạng thái'
    
    def activate_subscribers(self, request, queryset):
        """Kích hoạt lại các đăng ký"""
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'Đã kích hoạt {updated} đăng ký.')
    activate_subscribers.short_description = 'Kích hoạt đăng ký đã chọn'
    
    def deactivate_subscribers(self, request, queryset):
        """Hủy các đăng ký"""
        from django.utils import timezone
        for obj in queryset:
            obj.is_active = False
            obj.unsubscribed_at = timezone.now()
            obj.save()
        self.message_user(request, f'Đã hủy {queryset.count()} đăng ký.')
    deactivate_subscribers.short_description = 'Hủy đăng ký đã chọn'
