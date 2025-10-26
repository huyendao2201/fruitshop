from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="Đường dẫn")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Hình ảnh")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            from unidecode import unidecode
            import uuid
            # Chuyển tiếng Việt sang không dấu rồi slugify
            base_slug = slugify(unidecode(self.name))
            if not base_slug:  # Nếu slugify trả về rỗng
                base_slug = f"category-{uuid.uuid4().hex[:8]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="Đường dẫn")
    description = models.TextField(verbose_name="Mô tả chi tiết")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Mô tả ngắn")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá gốc")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Giá khuyến mãi")
    stock = models.PositiveIntegerField(default=0, verbose_name="Tồn kho")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Hình ảnh chính")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="Danh mục")
    
    # Các trường mới để quản lý sản phẩm tốt hơn
    unit = models.CharField(max_length=20, default='kg', help_text='VD: kg, cái, hộp', verbose_name="Đơn vị")
    origin = models.CharField(max_length=100, blank=True, help_text='Quốc gia/Vùng miền xuất xứ', verbose_name="Xuất xứ")
    nutrition_info = models.TextField(blank=True, help_text='Thông tin dinh dưỡng', verbose_name="Dinh dưỡng")
    
    # Các trường trạng thái
    is_active = models.BooleanField(default=True, verbose_name="Đang bán")
    is_featured = models.BooleanField(default=False, help_text='Hiển thị trên trang chủ', verbose_name="Nổi bật")
    is_new = models.BooleanField(default=False, verbose_name="Sản phẩm mới")
    is_bestseller = models.BooleanField(default=False, verbose_name="Bán chạy")
    is_hot = models.BooleanField(default=False, help_text='Sản phẩm HOT/Đang thịnh hành', verbose_name="HOT")
    
    # Các trường SEO
    meta_keywords = models.CharField(max_length=255, blank=True, verbose_name="Từ khóa SEO")
    meta_description = models.CharField(max_length=255, blank=True, verbose_name="Mô tả SEO")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            from unidecode import unidecode
            import uuid
            # Chuyển tiếng Việt sang không dấu rồi slugify
            base_slug = slugify(unidecode(self.name))
            if not base_slug:  # Nếu slugify trả về rỗng
                base_slug = f"product-{uuid.uuid4().hex[:8]}"
            self.slug = base_slug
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def get_price(self):
        """Trả về giá khuyến mãi nếu có, nếu không thì trả về giá gốc"""
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percentage(self):
        """Tính phần trăm giảm giá"""
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def average_rating(self):
        """Lấy đánh giá trung bình từ các review"""
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    @property
    def review_count(self):
        """Lấy tổng số lượng đánh giá"""
        return self.reviews.count()

    @property
    def stock_status(self):
        """Trả về thông báo trạng thái tồn kho"""
        if self.stock == 0:
            return "Hết hàng"
        elif self.stock < 10:
            return "Sắp hết"
        else:
            return "Còn hàng"

    @property
    def get_primary_image(self):
        """
        Lấy ảnh chính của sản phẩm theo thứ tự ưu tiên:
        1. Ảnh có is_primary=True từ ProductImage
        2. Ảnh đầu tiên trong ProductImage
        3. Ảnh từ field image của Product
        4. None nếu không có ảnh nào
        """
        # Ưu tiên: Ảnh có is_primary=True
        primary_img = self.images.filter(is_primary=True).first()
        if primary_img:
            return primary_img.image
        
        # Nếu không có, lấy ảnh đầu tiên
        first_img = self.images.first()
        if first_img:
            return first_img.image
        
        # Nếu vẫn không có, dùng ảnh từ field image
        return self.image


class ProductImage(models.Model):
    """Nhiều hình ảnh cho một sản phẩm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Sản phẩm")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Hình ảnh")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="Văn bản thay thế")
    is_primary = models.BooleanField(default=False, verbose_name="Ảnh chính")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Hình ảnh sản phẩm"
        verbose_name_plural = "Hình ảnh sản phẩm"
        ordering = ['order', '-is_primary', 'created_at']

    def __str__(self):
        return f"{self.product.name} - Ảnh {self.order}"


class Review(models.Model):
    """Đánh giá và xếp hạng sản phẩm"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sản phẩm")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Người dùng")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Đánh giá từ 1 đến 5 sao',
        verbose_name="Đánh giá"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    comment = models.TextField(verbose_name="Nội dung")
    is_verified_purchase = models.BooleanField(default=False, verbose_name="Đã mua hàng")
    is_approved = models.BooleanField(default=True, verbose_name="Đã duyệt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá sản phẩm"
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}★)"


class ShopReview(models.Model):
    """Đánh giá cửa hàng"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop_reviews', verbose_name="Người dùng")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Đánh giá từ 1 đến 5 sao',
        verbose_name="Đánh giá"
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    comment = models.TextField(verbose_name="Nội dung đánh giá")
    is_verified_purchase = models.BooleanField(default=False, verbose_name="Đã từng mua hàng")
    is_approved = models.BooleanField(default=True, verbose_name="Đã duyệt")
    is_featured = models.BooleanField(default=False, verbose_name="Hiển thị nổi bật")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đánh giá cửa hàng"
        verbose_name_plural = "Đánh giá cửa hàng"
        ordering = ['-created_at']
        # Mỗi user chỉ được đánh giá cửa hàng 1 lần
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_shop_review_per_user')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.rating}★ - {self.title}"


class Wishlist(models.Model):
    """Danh sách yêu thích của người dùng"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist', verbose_name="Người dùng")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")

    class Meta:
        verbose_name = "Yêu thích"
        verbose_name_plural = "Danh sách yêu thích"
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class Newsletter(models.Model):
    """Đăng ký nhận tin"""
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")
    unsubscribed_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày hủy đăng ký")
    
    class Meta:
        verbose_name = "Đăng ký nhận tin"
        verbose_name_plural = "Đăng ký nhận tin"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        status = "Đang hoạt động" if self.is_active else "Đã hủy"
        return f"{self.email} - {status}"


class Discount(models.Model):
    """Mã giảm giá và khuyến mãi"""
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Phần trăm'),
        ('fixed', 'Số tiền cố định'),
    )
    
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã giảm giá")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, default='percentage', verbose_name="Loại giảm giá")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá trị")
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Đơn hàng tối thiểu")
    max_uses = models.PositiveIntegerField(default=0, help_text='0 = không giới hạn', verbose_name="Số lần dùng tối đa")
    used_count = models.PositiveIntegerField(default=0, verbose_name="Đã sử dụng")
    
    valid_from = models.DateTimeField(verbose_name="Có hiệu lực từ")
    valid_to = models.DateTimeField(verbose_name="Có hiệu lực đến")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Mã giảm giá"
        verbose_name_plural = "Mã giảm giá"

    def __str__(self):
        return f"{self.code} - {self.value}{'%' if self.discount_type == 'percentage' else 'đ'}"

    @property
    def is_valid(self):
        """Kiểm tra xem mã giảm giá có còn hiệu lực không"""
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.max_uses > 0 and self.used_count >= self.max_uses:
            return False
        return True

    def calculate_discount(self, amount):
        """Tính số tiền giảm giá"""
        if not self.is_valid or amount < self.min_purchase:
            return 0
        
        if self.discount_type == 'percentage':
            return (amount * self.value) / 100
        else:
            return min(self.value, amount)
