from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import Order
from .models import Delivery


@receiver(post_save, sender=Order)
def create_delivery_for_order(sender, instance, created, **kwargs):
    """
    Tự động tạo Delivery ngay khi Order được tạo
    """
    # Tạo Delivery ngay khi Order được tạo (created=True)
    # hoặc khi Order chuyển sang trạng thái confirmed/processing/shipped mà chưa có Delivery
    should_create = (
        created or  # Mới tạo Order
        (instance.status in ['confirmed', 'processing', 'shipped'] and not hasattr(instance, 'delivery'))
    )
    
    if should_create:
        # Kiểm tra xem đã có Delivery chưa (tránh duplicate)
        try:
            _ = instance.delivery
            # Đã có Delivery rồi, không tạo nữa
            return
        except Delivery.DoesNotExist:
            # Chưa có Delivery, tạo mới
            pass
        
        # Địa chỉ lấy hàng mặc định (có thể cấu hình trong settings)
        pickup_address = "Kho Fresh Berry, 123 Đường Trần Hưng Đạo, Quận 1, TP.HCM"
        
        Delivery.objects.create(
            order=instance,
            pickup_address=pickup_address,
            delivery_address=instance.shipping_address,
            recipient_name=instance.user.get_full_name() or instance.user.username,
            recipient_phone=instance.phone,
            status='pending'  # Delivery cũng bắt đầu với status pending
        )
















