from django.contrib import admin
from django.utils.html import format_html
from products.models import Discount


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Quản trị mã giảm giá"""
    list_display = ('code', 'discount_display', 'valid_from', 'valid_to', 'used_count', 
                    'max_uses', 'is_valid_badge', 'is_active')
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_to')
    search_fields = ('code', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('used_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin giảm giá', {
            'fields': ('code', 'description', 'discount_type', 'value')
        }),
        ('Điều kiện', {
            'fields': ('min_purchase', 'max_uses', 'used_count')
        }),
        ('Thời hạn', {
            'fields': ('valid_from', 'valid_to', 'is_active')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def discount_display(self, obj):
        """Hiển thị giá trị giảm giá"""
        if obj.discount_type == 'percentage':
            return f"{obj.value}% OFF"
        else:
            return f"${obj.value} OFF"
    discount_display.short_description = 'Giảm giá'

    def is_valid_badge(self, obj):
        """Hiển thị trạng thái có hiệu lực"""
        if obj.is_valid:
            return format_html('<span style="color: green;">✅ Có hiệu lực</span>')
        return format_html('<span style="color: red;">❌ Hết hiệu lực</span>')
    is_valid_badge.short_description = 'Trạng thái'
