# TÀI LIỆU CHỨC NĂNG DỰ ÁN FRESHBERRY FRUIT SHOP

## TỔNG QUAN DỰ ÁN

**Tên dự án:** FreshBerry Fruit Shop  
**Công nghệ:** Django 5.2+ (Python)  
**Database:** MySQL  
**Mô tả:** Hệ thống bán trái cây trực tuyến với đầy đủ tính năng thương mại điện tử

---

## CÁC MODULE CHÍNH

### 1. ACCOUNTS (Quản lý tài khoản)

**Models:**
- `User`: Kế thừa AbstractUser với 2 vai trò
  - `admin`: Quản trị viên
  - `customer`: Khách hàng

**Chức năng:**
- ✅ Đăng ký tài khoản khách hàng
- ✅ Đăng nhập/Đăng xuất
- ✅ Xem và cập nhật thông tin cá nhân
- ✅ Quản lý địa chỉ giao hàng
- ✅ Xem lịch sử đơn hàng

**Thông tin user:**
- Username, Email, Password
- Họ tên (first_name, last_name)
- Số điện thoại, Địa chỉ
- Vai trò (role)

---

### 2. PRODUCTS (Quản lý sản phẩm)

**Models chính:**
- `Category`: Danh mục sản phẩm
- `Product`: Sản phẩm trái cây
- `ProductImage`: Nhiều ảnh cho mỗi sản phẩm
- `Review`: Đánh giá sản phẩm
- `ShopReview`: Đánh giá cửa hàng
- `Wishlist`: Danh sách yêu thích
- `Discount`: Mã giảm giá
- `Newsletter`: Đăng ký nhận tin

**Chức năng:**

#### 2.1 Danh mục (Category)
- Tên danh mục, mô tả, hình ảnh
- Slug tự động từ tiếng Việt
- Trạng thái hoạt động
- Đếm số lượng sản phẩm

#### 2.2 Sản phẩm (Product)
- **Thông tin cơ bản:**
  - Tên, slug, mô tả (ngắn/dài)
  - Giá gốc, giá khuyến mãi
  - Tồn kho, đơn vị tính (kg, cái, hộp)
  - Xuất xứ, thông tin dinh dưỡng
  - Hình ảnh chính + gallery

- **Phân loại sản phẩm:**
  - Sản phẩm nổi bật (Featured)
  - Sản phẩm mới (New)
  - Sản phẩm bán chạy (Bestseller)
  - Sản phẩm HOT (Hot)

- **SEO:**
  - Meta keywords, meta description

- **Tính năng:**
  - Tự động tính % giảm giá
  - Kiểm tra còn hàng/sắp hết
  - Đánh giá trung bình
  - Đếm số lượng review

#### 2.3 Đánh giá sản phẩm (Review)
- Đánh giá từ 1-5 sao
- Tiêu đề, nội dung
- Xác nhận đã mua hàng
- Duyệt đánh giá trước khi hiển thị

#### 2.4 Đánh giá cửa hàng (ShopReview)
- Đánh giá tổng thể cửa hàng
- Mỗi user chỉ được đánh giá 1 lần
- Chọn review nổi bật để hiển thị
- Xác nhận đã từng mua hàng

#### 2.5 Mã giảm giá (Discount)
- **Loại giảm giá:**
  - Phần trăm (percentage)
  - Số tiền cố định (fixed)
  
- **Điều kiện:**
  - Giá trị đơn hàng tối thiểu
  - Số lần sử dụng tối đa
  - Thời gian hiệu lực (từ-đến)
  - Trạng thái kích hoạt

- **Tính năng:**
  - Tự động kiểm tra hiệu lực
  - Tính toán giảm giá
  - Đếm số lần đã sử dụng

#### 2.6 Danh sách yêu thích (Wishlist)
- Lưu sản phẩm yêu thích
- Mỗi user-product chỉ có 1 bản ghi

#### 2.7 Newsletter
- Đăng ký nhận tin qua email
- Quản lý trạng thái đăng ký/hủy đăng ký

---

### 3. ORDERS (Quản lý đơn hàng)

**Models:**
- `Order`: Đơn hàng
- `OrderItem`: Chi tiết sản phẩm trong đơn
- `OrderTracking`: Theo dõi lịch sử đơn hàng

**Chức năng:**

#### 3.1 Giỏ hàng (Session-based)
- Thêm sản phẩm vào giỏ
- Cập nhật số lượng
- Xóa sản phẩm
- Xóa toàn bộ giỏ hàng
- Kiểm tra tồn kho

#### 3.2 Đặt hàng (Checkout)
- **Thông tin khách hàng:**
  - Địa chỉ giao hàng
  - Số điện thoại
  - Email
  - Ghi chú

- **Tính toán đơn hàng:**
  - Tạm tính (Subtotal)
  - Phí vận chuyển (tự động)
  - Giảm giá (nếu có mã)
  - Tổng cộng

- **Phương thức thanh toán:**
  - COD (Thanh toán khi nhận hàng)
  - VNPay (Cổng thanh toán trực tuyến)
  - Chuyển khoản ngân hàng
  - Thẻ tín dụng
  - Ví điện tử

#### 3.3 Trạng thái đơn hàng
1. **Pending** - Chờ xác nhận
2. **Confirmed** - Đã xác nhận
3. **Processing** - Đang xử lý
4. **Shipped** - Đã giao vận
5. **Delivered** - Đã giao hàng
6. **Completed** - Hoàn thành
7. **Canceled** - Đã hủy

#### 3.4 Trạng thái thanh toán
- Pending - Chờ thanh toán
- Paid - Đã thanh toán
- Failed - Thất bại
- Refunded - Đã hoàn tiền

#### 3.5 Tích hợp VNPay
- Tạo URL thanh toán
- Xử lý callback (Return URL)
- Xử lý IPN (Instant Payment Notification)
- Lưu thông tin giao dịch:
  - Mã giao dịch VNPay
  - Mã ngân hàng
  - Loại thẻ
  - Mã phản hồi
  - Thời gian thanh toán

#### 3.6 Quản lý đơn hàng
- Xem danh sách đơn hàng
- Xem chi tiết đơn hàng
- Theo dõi trạng thái
- Hủy đơn (nếu chưa xử lý)
- Gửi email xác nhận

#### 3.7 Mã đơn hàng
- Tự động sinh mã: `ORD-YYYYMMDD-XXXXXX`
- Unique cho mỗi đơn

---

### 4. DELIVERY (Quản lý giao hàng)

**Models:**
- `DeliveryPerson`: Nhân viên giao hàng
- `Delivery`: Thông tin giao hàng
- `DeliveryTracking`: Theo dõi chi tiết
- `DeliveryZone`: Khu vực giao hàng

**Chức năng:**

#### 4.1 Nhân viên giao hàng (DeliveryPerson)
- **Thông tin:**
  - Tài khoản liên kết
  - Số điện thoại
  - Loại phương tiện (xe máy, ô tô, xe đạp, xe tải)
  - Biển số xe
  - Trạng thái hoạt động

- **Thống kê:**
  - Đánh giá (rating)
  - Tổng số đơn đã giao
  - Số đơn giao thành công
  - Tỷ lệ thành công
  - Số đơn đang giao

#### 4.2 Giao hàng (Delivery)
- **Trạng thái:**
  1. Pending - Chờ phân công
  2. Assigned - Đã phân công
  3. Picked Up - Đã lấy hàng
  4. In Transit - Đang giao
  5. Delivered - Đã giao
  6. Failed - Giao thất bại
  7. Returned - Đã hoàn trả

- **Thông tin:**
  - Đơn hàng liên kết
  - Nhân viên giao hàng
  - Địa chỉ lấy hàng
  - Địa chỉ giao hàng
  - Tên người nhận, SĐT
  - Thời gian dự kiến
  - Lý do thất bại (nếu có)
  - Ảnh xác nhận giao hàng

- **Đánh giá:**
  - Khách hàng đánh giá shipper
  - Phản hồi từ khách hàng

- **Vị trí GPS** (có thể tích hợp)
  - Vĩ độ, kinh độ hiện tại

#### 4.3 Theo dõi giao hàng (DeliveryTracking)
- Log mỗi thay đổi trạng thái
- Thông điệp mô tả
- Tên địa điểm
- Vị trí GPS (tùy chọn)
- Hình ảnh minh họa
- Người thực hiện

#### 4.4 Khu vực giao hàng (DeliveryZone)
- Tên khu vực
- Phí giao hàng cơ bản
- Phí thêm mỗi km
- Thời gian giao dự kiến (giờ)
- Danh sách quận/huyện
- Trạng thái hoạt động

#### 4.5 Nghiệp vụ giao hàng
1. **Phân công:** Admin gán shipper cho đơn
2. **Lấy hàng:** Shipper xác nhận đã lấy hàng
3. **Đang giao:** Cập nhật trạng thái đang giao
4. **Giao thành công:** Upload ảnh chứng minh
5. **Giao thất bại:** Nhập lý do thất bại

---

### 5. REPORTS (Admin Dashboard - Báo cáo và quản trị)

**Chức năng dành cho Admin:**

#### 5.1 Dashboard Tổng quan
- **Thống kê tổng:**
  - Tổng doanh thu (tất cả thời gian)
  - Doanh thu tháng
  - Tăng trưởng theo tháng (%)
  - Tổng đơn hàng
  - Đơn hàng tháng
  - Đơn hàng chờ xử lý
  - Tổng khách hàng
  - Khách hàng mới tháng này
  - Tổng sản phẩm
  - Sản phẩm đang bán

- **Biểu đồ:**
  - Doanh thu 12 tháng
  - Doanh thu 30 ngày
  - Phân bố trạng thái đơn hàng
  - Top sản phẩm bán chạy
  - Thống kê theo danh mục

- **Danh sách:**
  - 10 đơn hàng mới nhất
  - 20 sản phẩm đã bán gần đây
  - Top 5 sản phẩm bán chạy
  - 5 sản phẩm tồn kho thấp
  - 5 đánh giá mới nhất
  - Đánh giá cửa hàng
  - Thống kê giao hàng
  - Top 5 shipper

#### 5.2 Quản lý Sản phẩm
- Danh sách sản phẩm (phân trang)
- Tìm kiếm theo tên, mô tả
- Lọc theo danh mục, trạng thái
- Sắp xếp theo nhiều tiêu chí
- Thêm/Sửa/Xóa sản phẩm
- Quản lý gallery ảnh
- Đặt ảnh chính
- Xem thống kê bán hàng
- Xem lịch sử đánh giá

#### 5.3 Quản lý Đơn hàng
- Danh sách đơn hàng (phân trang)
- Tìm kiếm theo mã đơn, khách hàng, SĐT
- Lọc theo trạng thái, thanh toán
- Lọc theo khoảng thời gian
- Xem chi tiết đơn hàng
- Cập nhật trạng thái
- Xem thông tin giao hàng
- Phân công shipper
- Gửi email thông báo

#### 5.4 Quản lý Khách hàng
- Danh sách khách hàng
- Tìm kiếm theo email, tên, SĐT
- Xem chi tiết khách hàng
- Lịch sử mua hàng
- Tổng chi tiêu
- Đánh giá đã viết

#### 5.5 Quản lý Danh mục
- Thêm/Sửa/Xóa danh mục
- Xem số lượng sản phẩm
- Doanh thu theo danh mục
- Upload hình ảnh danh mục

#### 5.6 Quản lý Đánh giá
- Danh sách đánh giá sản phẩm
- Danh sách đánh giá cửa hàng
- Duyệt/Ẩn đánh giá
- Đặt đánh giá nổi bật
- Xóa đánh giá spam
- Xác nhận đã mua hàng

#### 5.7 Quản lý Mã giảm giá
- Thêm/Sửa/Xóa mã giảm giá
- Bật/Tắt mã giảm giá
- Xem thống kê sử dụng
- Doanh thu từ mã giảm giá

#### 5.8 Quản lý Giao hàng
- Danh sách delivery
- Lọc theo trạng thái, shipper
- Phân công shipper
- Cập nhật trạng thái giao hàng
- Xem tracking logs
- Quản lý shipper
- Thống kê hiệu suất shipper

#### 5.9 Quản lý Users (All roles)
- Danh sách tất cả users
- Lọc theo role (admin, staff, shipper, customer)
- Thêm/Sửa/Xóa user
- Phân quyền (groups)
- Bật/Tắt tài khoản
- Reset mật khẩu

#### 5.10 Báo cáo nâng cao
- Tùy chọn khoảng thời gian
- Doanh thu theo ngày
- Top sản phẩm theo doanh thu
- Phân tích theo danh mục
- Top khách hàng
- Xu hướng khách hàng mới
- Phân tích phương thức thanh toán
- Giá trị đơn hàng trung bình

#### 5.11 Export báo cáo
- Export CSV với encoding UTF-8 (có BOM)
- **Các loại báo cáo:**
  - Báo cáo đơn hàng
  - Báo cáo sản phẩm
  - Báo cáo khách hàng
  - Báo cáo doanh thu

#### 5.12 Quản lý Newsletter
- Danh sách email đăng ký
- Lọc theo trạng thái
- Bật/Tắt đăng ký
- Xóa email
- Thống kê đăng ký mới

---

## TÍNH NĂNG KHÁC

### Email Notifications
- Xác nhận đơn hàng
- Cập nhật trạng thái đơn hàng
- Phân công giao hàng cho shipper

### Session Cart
- Giỏ hàng lưu trong session
- Không cần đăng nhập để thêm vào giỏ
- Tự động tính toán

### SEO-Friendly URLs
- Slug tự động từ tiếng Việt
- URL thân thiện cho sản phẩm, danh mục

### Responsive Design
- Giao diện hiện đại
- Tương thích mobile

### Security
- CSRF Protection
- Authentication & Authorization
- Password hashing
- SQL Injection protection (Django ORM)

---

## THÔNG TIN ĐĂNG NHẬP MẶC ĐỊNH

```
Username: admin
Password: admin123
Email: admin@freshberry.vn
Role: Quản trị viên
```

---

## CÁC URL QUAN TRỌNG

```
Trang chủ:              http://127.0.0.1:8000/
Admin Dashboard:        http://127.0.0.1:8000/reports/dashboard/
Django Admin:           http://127.0.0.1:8000/admin/
Sản phẩm:              http://127.0.0.1:8000/products/
Giỏ hàng:              http://127.0.0.1:8000/orders/cart/
Đơn hàng:              http://127.0.0.1:8000/orders/
Tài khoản:             http://127.0.0.1:8000/accounts/
```

---

## CÔNG NGHỆ SỬ DỤNG

- **Backend:** Django 5.2+
- **Database:** MySQL (mysqlclient)
- **Frontend:** HTML, CSS, JavaScript (jQuery)
- **Image Processing:** Pillow
- **Text Processing:** Unidecode (xử lý tiếng Việt)
- **HTTP Requests:** requests
- **Payment Gateway:** VNPay

---

## QUY TRÌNH NGHIỆP VỤ CHÍNH

### 1. Quy trình Mua hàng (Customer)
```
1. Duyệt sản phẩm/tìm kiếm
2. Xem chi tiết sản phẩm
3. Thêm vào giỏ hàng
4. Cập nhật số lượng (tùy chọn)
5. Đăng nhập (nếu chưa)
6. Checkout - nhập thông tin giao hàng
7. Áp dụng mã giảm giá (tùy chọn)
8. Chọn phương thức thanh toán
9. Xác nhận đơn hàng
10. Thanh toán (VNPay hoặc COD)
11. Nhận email xác nhận
12. Theo dõi đơn hàng
```

### 2. Quy trình Xử lý đơn hàng (Admin)
```
1. Nhận đơn hàng mới (Pending)
2. Kiểm tra và xác nhận đơn (Confirmed)
3. Chuẩn bị hàng (Processing)
4. Tạo phiếu giao hàng
5. Phân công shipper
6. Shipper lấy hàng (Picked Up)
7. Shipper giao hàng (In Transit)
8. Giao thành công (Delivered)
9. Hoàn thành đơn (Completed)
10. Khách hàng đánh giá (tùy chọn)
```

### 3. Quy trình Giao hàng (Shipper)
```
1. Nhận thông báo phân công (email)
2. Xem thông tin đơn hàng
3. Xác nhận đã lấy hàng
4. Cập nhật đang giao hàng
5. Cập nhật vị trí (tùy chọn)
6. Giao hàng thành công:
   - Upload ảnh chứng minh
   - Thu tiền (nếu COD)
7. Hoặc giao thất bại:
   - Nhập lý do
   - Hoàn hàng về kho
```

---

## KẾT LUẬN

Đây là một hệ thống bán hàng trực tuyến hoàn chỉnh với đầy đủ các tính năng:
- ✅ Quản lý sản phẩm đa dạng
- ✅ Giỏ hàng và thanh toán linh hoạt
- ✅ Tích hợp cổng thanh toán VNPay
- ✅ Hệ thống giao hàng chuyên nghiệp
- ✅ Admin dashboard mạnh mẽ với báo cáo chi tiết
- ✅ Đánh giá sản phẩm và cửa hàng
- ✅ Mã giảm giá linh hoạt
- ✅ Email notifications tự động
- ✅ Quản lý user đa vai trò

Hệ thống có thể mở rộng thêm:
- Tích hợp SMS
- Real-time GPS tracking
- Mobile app
- AI recommendation system
- Advanced analytics
- Multi-language support

