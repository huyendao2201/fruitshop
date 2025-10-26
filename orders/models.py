from django.db import models
from django.conf import settings
from products.models import Product
import uuid


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('processing', 'Đang xử lý'),
        ('shipped', 'Đã giao vận'),
        ('delivered', 'Đã giao hàng'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('cod', 'Thanh toán khi nhận hàng'),
        ('vnpay', 'Thanh toán VNPay'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('credit_card', 'Thẻ tín dụng'),
        ('e_wallet', 'Ví điện tử'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
        ('refunded', 'Đã hoàn tiền'),
    )
    
    # Nhận diện đơn hàng
    order_number = models.CharField(max_length=50, unique=True, editable=False, blank=True, verbose_name="Mã đơn hàng")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Khách hàng")
    
    # Chi tiết đơn hàng
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Trạng thái thanh toán")
    
    # Giá cả
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tạm tính")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Giảm giá")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Phí vận chuyển")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Tổng cộng")
    
    # Mã giảm giá
    discount_code = models.CharField(max_length=50, blank=True, verbose_name="Mã giảm giá")
    
    # Thông tin giao hàng
    shipping_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    notes = models.TextField(blank=True, help_text='Ghi chú từ khách hàng', verbose_name="Ghi chú")
    
    # Theo dõi
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Mã vận đơn")
    estimated_delivery = models.DateField(blank=True, null=True, verbose_name="Ngày giao dự kiến")
    
    # Các trường thanh toán VNPay
    vnpay_transaction_id = models.CharField(max_length=100, blank=True, verbose_name="Mã giao dịch VNPay")
    vnpay_transaction_no = models.CharField(max_length=100, blank=True, verbose_name="Mã GD tại VNPAY")
    vnpay_bank_code = models.CharField(max_length=20, blank=True, verbose_name="Mã ngân hàng")
    vnpay_card_type = models.CharField(max_length=20, blank=True, verbose_name="Loại thẻ")
    vnpay_response_code = models.CharField(max_length=10, blank=True, verbose_name="Mã phản hồi")
    vnpay_paid_at = models.DateTimeField(blank=True, null=True, verbose_name="Thời gian thanh toán VNPay")
    
    # Thời gian
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày xác nhận")
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày giao vận")
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày giao hàng")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Tạo mã đơn hàng duy nhất"""
        from django.utils import timezone
        while True:
            date_str = timezone.now().strftime('%Y%m%d')
            random_str = str(uuid.uuid4().hex)[:6].upper()
            order_number = f"ORD-{date_str}-{random_str}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def __str__(self):
        return f"{self.order_number} - {self.user.username}"

    def calculate_total(self):
        """Tính tổng đơn hàng"""
        self.subtotal = sum(item.get_total_price() for item in self.items.all())
        self.total_amount = self.subtotal - self.discount_amount + self.shipping_fee
        self.save()
        return self.total_amount

    @property
    def item_count(self):
        """Tổng số sản phẩm trong đơn hàng"""
        return sum(item.quantity for item in self.items.all())

    @property
    def status_display(self):
        """Lấy hiển thị trạng thái kèm icon"""
        status_icons = {
            'pending': '⏳',
            'confirmed': '✅',
            'processing': '📦',
            'shipped': '🚚',
            'delivered': '✨',
            'completed': '🎉',
            'canceled': '❌',
        }
        return f"{status_icons.get(self.status, '')} {self.get_status_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Đơn hàng")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Giá")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Giá khuyến mãi")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """Tính tổng giá cho mục này"""
        if self.discount_price:
            unit_price = self.discount_price
        elif self.price:
            unit_price = self.price
        else:
            return 0
        
        if self.quantity:
            return self.quantity * unit_price
        return 0

    def get_saved_amount(self):
        """Tính số tiền tiết kiệm được nếu có giảm giá"""
        if self.discount_price and self.price and self.quantity:
            if self.discount_price < self.price:
                return (self.price - self.discount_price) * self.quantity
        return 0
    
    @property
    def saved_amount(self):
        """Property wrapper cho get_saved_amount"""
        return self.get_saved_amount()


class OrderTracking(models.Model):
    """Theo dõi thay đổi trạng thái đơn hàng"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tracking', verbose_name="Đơn hàng")
    status = models.CharField(max_length=20, verbose_name="Trạng thái")
    message = models.TextField(verbose_name="Thông điệp")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người thực hiện")

    class Meta:
        verbose_name = "Theo dõi đơn hàng"
        verbose_name_plural = "Theo dõi đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order.order_number} - {self.status} lúc {self.created_at}"
