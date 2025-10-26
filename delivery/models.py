from django.db import models
from django.conf import settings
from django.utils import timezone
from orders.models import Order


class DeliveryPerson(models.Model):
    """Nhân viên giao hàng"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='delivery_person',
        verbose_name="Tài khoản"
    )
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('motorbike', 'Xe máy'),
            ('car', 'Ô tô'),
            ('bicycle', 'Xe đạp'),
            ('truck', 'Xe tải'),
        ],
        default='motorbike',
        verbose_name="Loại phương tiện"
    )
    vehicle_number = models.CharField(max_length=20, blank=True, verbose_name="Biển số xe")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0, verbose_name="Đánh giá")
    total_deliveries = models.IntegerField(default=0, verbose_name="Tổng số đơn đã giao")
    successful_deliveries = models.IntegerField(default=0, verbose_name="Số đơn giao thành công")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Nhân viên giao hàng"
        verbose_name_plural = "Nhân viên giao hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.phone}"
    
    @property
    def success_rate(self):
        """Tỷ lệ giao hàng thành công"""
        if self.total_deliveries == 0:
            return 0
        return (self.successful_deliveries / self.total_deliveries) * 100
    
    @property
    def current_deliveries(self):
        """Số đơn đang giao"""
        return self.deliveries.filter(
            status__in=['assigned', 'picked_up', 'in_transit']
        ).count()


class Delivery(models.Model):
    """Thông tin giao hàng"""
    STATUS_CHOICES = [
        ('pending', 'Chờ phân công'),
        ('assigned', 'Đã phân công'),
        ('picked_up', 'Đã lấy hàng'),
        ('in_transit', 'Đang giao'),
        ('delivered', 'Đã giao'),
        ('failed', 'Giao thất bại'),
        ('returned', 'Đã hoàn trả'),
    ]
    
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery',
        verbose_name="Đơn hàng"
    )
    delivery_person = models.ForeignKey(
        DeliveryPerson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries',
        verbose_name="Nhân viên giao hàng"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Trạng thái"
    )
    
    # Thông tin giao hàng
    pickup_address = models.TextField(verbose_name="Địa chỉ lấy hàng")
    delivery_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    recipient_name = models.CharField(max_length=100, verbose_name="Tên người nhận")
    recipient_phone = models.CharField(max_length=15, verbose_name="SĐT người nhận")
    
    # Thời gian
    assigned_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian phân công")
    picked_up_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian lấy hàng")
    estimated_delivery_time = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian giao dự kiến")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian giao thực tế")
    
    # Ghi chú và lý do
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    failure_reason = models.TextField(blank=True, verbose_name="Lý do thất bại")
    
    # Hình ảnh xác nhận
    delivery_proof_image = models.ImageField(
        upload_to='delivery_proofs/',
        blank=True,
        null=True,
        verbose_name="Ảnh xác nhận giao hàng"
    )
    
    # Đánh giá
    customer_rating = models.IntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Đánh giá của khách hàng"
    )
    customer_feedback = models.TextField(blank=True, verbose_name="Phản hồi của khách hàng")
    
    # Vị trí hiện tại (có thể tích hợp GPS sau)
    current_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Vĩ độ hiện tại"
    )
    current_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Kinh độ hiện tại"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Giao hàng"
        verbose_name_plural = "Giao hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Giao hàng #{self.id} - Đơn {self.order.order_number}"
    
    @property
    def is_delayed(self):
        """Kiểm tra xem có bị trễ không"""
        if self.estimated_delivery_time and not self.delivered_at:
            return timezone.now() > self.estimated_delivery_time
        return False
    
    @property
    def delivery_duration(self):
        """Thời gian giao hàng (từ lúc lấy đến lúc giao)"""
        if self.picked_up_at and self.delivered_at:
            return self.delivered_at - self.picked_up_at
        return None
    
    def assign_to_person(self, delivery_person):
        """Phân công cho nhân viên giao hàng"""
        self.delivery_person = delivery_person
        self.status = 'assigned'
        self.assigned_at = timezone.now()
        self.save()
        
        # Tạo nhật ký theo dõi
        DeliveryTracking.objects.create(
            delivery=self,
            status='assigned',
            message=f'Đơn hàng được phân công cho {delivery_person.user.get_full_name()}',
            location_name='Kho hàng',
            created_by=delivery_person.user
        )
        
        # Gửi email thông báo cho nhân viên giao hàng
        try:
            from orders.utils import send_delivery_assignment_email
            send_delivery_assignment_email(self)
        except Exception as e:
            print(f"Failed to send delivery assignment email: {e}")
    
    def mark_picked_up(self, user=None):
        """Đánh dấu đã lấy hàng"""
        self.status = 'picked_up'
        self.picked_up_at = timezone.now()
        self.save()
        
        DeliveryTracking.objects.create(
            delivery=self,
            status='picked_up',
            message='Đã lấy hàng từ kho',
            location_name='Kho hàng',
            created_by=user or self.delivery_person.user
        )
    
    def mark_in_transit(self, user=None):
        """Đánh dấu đang giao"""
        self.status = 'in_transit'
        self.save()
        
        DeliveryTracking.objects.create(
            delivery=self,
            status='in_transit',
            message='Đang trên đường giao hàng',
            created_by=user or self.delivery_person.user
        )
    
    def mark_delivered(self, user=None, proof_image=None):
        """Đánh dấu đã giao thành công"""
        self.status = 'delivered'
        self.delivered_at = timezone.now()
        if proof_image:
            self.delivery_proof_image = proof_image
        self.save()
        
        # Cập nhật order status
        self.order.status = 'delivered'
        self.order.delivered_at = timezone.now()
        
        # Nếu là COD (thanh toán khi nhận hàng), tự động đánh dấu đã thanh toán
        if self.order.payment_method == 'cod':
            self.order.payment_status = 'paid'
        
        self.order.save()
        
        # Cập nhật thống kê nhân viên giao hàng
        if self.delivery_person:
            self.delivery_person.total_deliveries += 1
            self.delivery_person.successful_deliveries += 1
            self.delivery_person.save()
        
        DeliveryTracking.objects.create(
            delivery=self,
            status='delivered',
            message='Giao hàng thành công',
            location_name=self.delivery_address,
            created_by=user or self.delivery_person.user
        )
    
    def mark_failed(self, reason, user=None):
        """Đánh dấu giao thất bại"""
        self.status = 'failed'
        self.failure_reason = reason
        self.save()
        
        # Cập nhật thống kê
        if self.delivery_person:
            self.delivery_person.total_deliveries += 1
            self.delivery_person.save()
        
        DeliveryTracking.objects.create(
            delivery=self,
            status='failed',
            message=f'Giao hàng thất bại: {reason}',
            created_by=user or self.delivery_person.user
        )


class DeliveryTracking(models.Model):
    """Theo dõi chi tiết quá trình giao hàng"""
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='tracking_logs',
        verbose_name="Giao hàng"
    )
    status = models.CharField(max_length=20, verbose_name="Trạng thái")
    message = models.TextField(verbose_name="Thông điệp")
    location_name = models.CharField(max_length=255, blank=True, verbose_name="Tên địa điểm")
    
    # Vị trí GPS
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Vĩ độ"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="Kinh độ"
    )
    
    image = models.ImageField(
        upload_to='delivery_tracking/',
        blank=True,
        null=True,
        verbose_name="Hình ảnh"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Người tạo"
    )
    
    class Meta:
        verbose_name = "Theo dõi giao hàng"
        verbose_name_plural = "Theo dõi giao hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.delivery} - {self.status} lúc {self.created_at}"


class DeliveryZone(models.Model):
    """Khu vực giao hàng"""
    name = models.CharField(max_length=100, verbose_name="Tên khu vực")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    # Phí giao hàng
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Phí cơ bản")
    additional_fee_per_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Phí thêm mỗi km"
    )
    
    # Thời gian giao hàng dự kiến (giờ)
    estimated_delivery_hours = models.IntegerField(default=24, verbose_name="Thời gian giao dự kiến (giờ)")
    
    # Khu vực có thể giao
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    # Danh sách quận/huyện (có thể mở rộng thành bảng riêng)
    districts = models.TextField(
        help_text="Danh sách quận/huyện, mỗi dòng một quận",
        verbose_name="Danh sách quận/huyện"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Khu vực giao hàng"
        verbose_name_plural = "Khu vực giao hàng"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.base_fee}đ"
    
    def get_districts_list(self):
        """Lấy danh sách quận/huyện"""
        return [d.strip() for d in self.districts.split('\n') if d.strip()]
