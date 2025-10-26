from django.contrib import admin
from .models import DeliveryPerson, Delivery, DeliveryTracking, DeliveryZone


@admin.register(DeliveryPerson)
class DeliveryPersonAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'vehicle_type', 'is_active', 'rating', 'success_rate', 'current_deliveries']
    list_filter = ['is_active', 'vehicle_type']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['total_deliveries', 'successful_deliveries', 'created_at', 'updated_at']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'delivery_person', 'status', 'recipient_name', 'is_delayed', 'created_at']
    list_filter = ['status', 'created_at', 'assigned_at']
    search_fields = ['order__order_number', 'recipient_name', 'recipient_phone']
    readonly_fields = ['created_at', 'updated_at', 'assigned_at', 'picked_up_at', 'delivered_at']
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('order', 'delivery_person', 'status')
        }),
        ('Thông tin giao hàng', {
            'fields': ('pickup_address', 'delivery_address', 'recipient_name', 'recipient_phone')
        }),
        ('Thời gian', {
            'fields': ('assigned_at', 'picked_up_at', 'estimated_delivery_time', 'delivered_at')
        }),
        ('Chi tiết', {
            'fields': ('notes', 'failure_reason', 'delivery_proof_image')
        }),
        ('Đánh giá', {
            'fields': ('customer_rating', 'customer_feedback')
        }),
        ('Vị trí', {
            'fields': ('current_latitude', 'current_longitude'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeliveryTracking)
class DeliveryTrackingAdmin(admin.ModelAdmin):
    list_display = ['delivery', 'status', 'message', 'location_name', 'created_at', 'created_by']
    list_filter = ['status', 'created_at']
    search_fields = ['delivery__order__order_number', 'message', 'location_name']
    readonly_fields = ['created_at']


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_fee', 'estimated_delivery_hours', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'districts']
