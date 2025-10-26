from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem, OrderTracking


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price', 'saved_amount')
    fields = ('product', 'quantity', 'price', 'discount_price', 'get_total_price', 'saved_amount')
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Auto-populate price from product when adding new items
        class OrderItemFormset(formset):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                for form in self.forms:
                    if form.instance.pk is None and form.instance.product_id:
                        # New item - populate price from product
                        try:
                            product = form.instance.product
                            if not form.instance.price:
                                form.instance.price = product.price
                            if product.discount_price and not form.instance.discount_price:
                                form.instance.discount_price = product.discount_price
                        except:
                            pass
        return OrderItemFormset

    def get_total_price(self, obj):
        if obj and obj.pk:
            try:
                total = obj.get_total_price()
                if total is not None:
                    return format_html('${:.2f}', float(total))
            except (TypeError, ValueError, AttributeError):
                pass
        return '-'
    get_total_price.short_description = 'Total Price'

    def saved_amount(self, obj):
        if obj and obj.pk:
            try:
                saved = obj.saved_amount
                if saved and saved > 0:
                    return format_html('<span style="color: green;">${:.2f}</span>', float(saved))
            except (TypeError, ValueError, AttributeError):
                pass
        return '-'
    saved_amount.short_description = 'Saved'


class OrderTrackingInline(admin.TabularInline):
    model = OrderTracking
    extra = 1
    fields = ('status', 'message', 'created_by', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status_badge', 'payment_status_badge', 
                    'subtotal_display', 'discount_display', 'total_display', 'created_at')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__username', 'user__email', 'phone', 'discount_code')
    readonly_fields = ('order_number', 'subtotal', 'discount_amount', 'total_amount', 
                      'item_count', 'created_at', 'updated_at', 'confirmed_at', 
                      'shipped_at', 'delivered_at')
    inlines = [OrderItemInline, OrderTrackingInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_method', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'discount_code', 'discount_amount', 'shipping_fee', 'total_amount', 'item_count')
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'phone', 'email', 'notes')
        }),
        ('Tracking', {
            'fields': ('tracking_number', 'estimated_delivery')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_completed']

    def status_badge(self, obj):
        color_map = {
            'pending': '#FFA500',
            'confirmed': '#4CAF50',
            'processing': '#2196F3',
            'shipped': '#9C27B0',
            'delivered': '#00BCD4',
            'completed': '#4CAF50',
            'canceled': '#F44336',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color_map.get(obj.status, '#999'), obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def payment_status_badge(self, obj):
        color_map = {
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'refunded': 'gray',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color_map.get(obj.payment_status, 'black'), obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'

    def subtotal_display(self, obj):
        return format_html('${:.2f}', float(obj.subtotal or 0))
    subtotal_display.short_description = 'Subtotal'

    def discount_display(self, obj):
        if obj.discount_amount and obj.discount_amount > 0:
            return format_html('<span style="color: green;">-${:.2f}</span>', float(obj.discount_amount))
        return '-'
    discount_display.short_description = 'Discount'

    def total_display(self, obj):
        return format_html('<strong>${:.2f}</strong>', float(obj.total_amount or 0))
    total_display.short_description = 'Total'

    def save_model(self, request, obj, form, change):
        from orders.utils import send_order_status_update_email
        
        # Track status changes
        if change and 'status' in form.changed_data:
            old_status = Order.objects.get(pk=obj.pk).status
            if old_status != obj.status:
                # Update timestamp fields
                if obj.status == 'confirmed' and not obj.confirmed_at:
                    obj.confirmed_at = timezone.now()
                elif obj.status == 'shipped' and not obj.shipped_at:
                    obj.shipped_at = timezone.now()
                elif obj.status == 'delivered' and not obj.delivered_at:
                    obj.delivered_at = timezone.now()
                
                # Create tracking entry
                OrderTracking.objects.create(
                    order=obj,
                    status=obj.status,
                    message=f"Order status changed from {old_status} to {obj.status}",
                    created_by=request.user
                )
                
                # Save first to ensure all fields are updated
                super().save_model(request, obj, form, change)
                obj.calculate_total()
                
                # Send email notification
                try:
                    send_order_status_update_email(obj, old_status, obj.status)
                    self.message_user(request, f'Email notification sent to {obj.email}', level='SUCCESS')
                except Exception as e:
                    self.message_user(request, f'Failed to send email: {str(e)}', level='WARNING')
                
                return
        
        super().save_model(request, obj, form, change)
        obj.calculate_total()

    # Admin actions
    def mark_as_confirmed(self, request, queryset):
        from orders.utils import send_order_status_update_email
        count = 0
        for order in queryset:
            old_status = order.status
            order.status = 'confirmed'
            order.confirmed_at = timezone.now()
            order.save()
            try:
                send_order_status_update_email(order, old_status, 'confirmed')
                count += 1
            except:
                pass
        self.message_user(request, f'{count} orders marked as confirmed and emails sent.')
    mark_as_confirmed.short_description = 'Mark as Confirmed (with email)'

    def mark_as_processing(self, request, queryset):
        from orders.utils import send_order_status_update_email
        count = 0
        for order in queryset:
            old_status = order.status
            order.status = 'processing'
            order.save()
            try:
                send_order_status_update_email(order, old_status, 'processing')
                count += 1
            except:
                pass
        self.message_user(request, f'{count} orders marked as processing and emails sent.')
    mark_as_processing.short_description = 'Mark as Processing (with email)'

    def mark_as_shipped(self, request, queryset):
        from orders.utils import send_order_status_update_email
        count = 0
        for order in queryset:
            old_status = order.status
            order.status = 'shipped'
            order.shipped_at = timezone.now()
            order.save()
            try:
                send_order_status_update_email(order, old_status, 'shipped')
                count += 1
            except:
                pass
        self.message_user(request, f'{count} orders marked as shipped and emails sent.')
    mark_as_shipped.short_description = 'Mark as Shipped (with email)'

    def mark_as_delivered(self, request, queryset):
        from orders.utils import send_order_status_update_email
        count = 0
        for order in queryset:
            old_status = order.status
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            try:
                send_order_status_update_email(order, old_status, 'delivered')
                count += 1
            except:
                pass
        self.message_user(request, f'{count} orders marked as delivered and emails sent.')
    mark_as_delivered.short_description = 'Mark as Delivered (with email)'

    def mark_as_completed(self, request, queryset):
        from orders.utils import send_order_status_update_email
        count = 0
        for order in queryset:
            old_status = order.status
            order.status = 'completed'
            order.save()
            try:
                send_order_status_update_email(order, old_status, 'completed')
                count += 1
            except:
                pass
        self.message_user(request, f'{count} orders marked as completed and emails sent.')
    mark_as_completed.short_description = 'Mark as Completed (with email)'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'discount_price', 'total_price', 'saved_display')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('product__name', 'order__order_number', 'order__user__username')
    
    def total_price(self, obj):
        if obj and obj.pk:
            try:
                total = obj.get_total_price()
                if total is not None:
                    return format_html('${:.2f}', float(total))
            except (TypeError, ValueError, AttributeError):
                pass
        return '-'
    total_price.short_description = 'Total Price'

    def saved_display(self, obj):
        if obj and obj.pk:
            try:
                saved = obj.saved_amount
                if saved and saved > 0:
                    return format_html('<span style="color: green; font-weight: bold;">${:.2f}</span>', float(saved))
            except (TypeError, ValueError, AttributeError):
                pass
        return '-'
    saved_display.short_description = 'Saved'


@admin.register(OrderTracking)
class OrderTrackingAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'message', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'message')
    readonly_fields = ('created_at',)
