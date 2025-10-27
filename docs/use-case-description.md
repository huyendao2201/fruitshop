# MÔ TẢ CHI TIẾT CÁC USE CASE - FRESHBERRY FRUIT SHOP

## TỔNG QUAN

Hệ thống FreshBerry Fruit Shop có **4 Actor chính**:
1. **Khách hàng (Customer)** - Người mua hàng
2. **Quản trị viên (Admin)** - Người quản lý hệ thống
3. **Nhân viên giao hàng (Shipper)** - Người giao hàng
4. **Hệ thống bên ngoài** - VNPay, Email

Tổng cộng: **46+ Use Cases** được nhóm thành **7 Package chức năng**

---

## 📦 PACKAGE 1: QUẢN LÝ TÀI KHOẢN (6 Use Cases)

### UC1: Đăng ký tài khoản
- **Actor:** Khách hàng
- **Mô tả:** Người dùng mới tạo tài khoản
- **Luồng chính:**
  1. Nhập username, email, password
  2. Nhập họ tên, số điện thoại
  3. Xác nhận đăng ký
  4. Hệ thống tạo tài khoản với role = "customer"
  5. Chuyển đến trang đăng nhập

### UC2: Đăng nhập
- **Actor:** Khách hàng, Admin, Shipper
- **Mô tả:** Người dùng đăng nhập vào hệ thống
- **Luồng chính:**
  1. Nhập username/email và password
  2. Hệ thống xác thực
  3. Tạo session
  4. Chuyển đến trang tương ứng với role

### UC3: Đăng xuất
- **Actor:** Khách hàng, Admin, Shipper
- **Mô tả:** Người dùng thoát khỏi hệ thống
- **Luồng chính:**
  1. Click nút đăng xuất
  2. Hệ thống xóa session
  3. Chuyển về trang chủ

### UC4: Xem thông tin cá nhân
- **Actor:** Khách hàng
- **Mô tả:** Xem profile của mình
- **Luồng chính:**
  1. Vào trang profile
  2. Hiển thị: Họ tên, Email, SĐT, Địa chỉ
  3. Hiển thị lịch sử đơn hàng

### UC5: Cập nhật thông tin
- **Actor:** Khách hàng
- **Mô tả:** Chỉnh sửa thông tin cá nhân
- **Luồng chính:**
  1. Vào form chỉnh sửa
  2. Cập nhật thông tin
  3. Lưu thay đổi

### UC6: Quản lý địa chỉ
- **Actor:** Khách hàng
- **Mô tả:** Quản lý địa chỉ giao hàng
- **Luồng chính:**
  1. Xem danh sách địa chỉ
  2. Thêm/Sửa/Xóa địa chỉ
  3. Đặt địa chỉ mặc định

---

## 📦 PACKAGE 2: QUẢN LÝ SẢN PHẨM (11 Use Cases)

### UC10: Xem danh sách sản phẩm
- **Actor:** Khách hàng
- **Mô tả:** Duyệt tất cả sản phẩm
- **Luồng chính:**
  1. Vào trang sản phẩm
  2. Hiển thị grid sản phẩm (phân trang)
  3. Hiển thị: Ảnh, Tên, Giá, Đánh giá
  4. Lọc/Sắp xếp

### UC11: Tìm kiếm sản phẩm
- **Actor:** Khách hàng
- **Mô tả:** Tìm sản phẩm theo từ khóa
- **Luồng chính:**
  1. Nhập từ khóa vào search box
  2. Tìm trong tên, mô tả
  3. Hiển thị kết quả

### UC12: Xem chi tiết sản phẩm
- **Actor:** Khách hàng
- **Mô tả:** Xem thông tin đầy đủ của sản phẩm
- **Luồng chính:**
  1. Click vào sản phẩm
  2. Hiển thị:
     - Gallery ảnh
     - Tên, Giá, Giảm giá
     - Mô tả chi tiết
     - Thông tin dinh dưỡng
     - Xuất xứ, Đơn vị
     - Đánh giá khách hàng
  3. Nút "Thêm vào giỏ"

### UC13: Lọc theo danh mục
- **Actor:** Khách hàng
- **Mô tả:** Lọc sản phẩm theo category
- **Luồng chính:**
  1. Chọn danh mục (Trái cây tươi, Sấy khô, Gift box...)
  2. Hiển thị sản phẩm thuộc danh mục
  3. Có thể lọc thêm: Giá, Đánh giá, Mới, HOT

### UC14: Thêm vào yêu thích
- **Actor:** Khách hàng (đã login)
- **Mô tả:** Lưu sản phẩm yêu thích
- **Luồng chính:**
  1. Click icon trái tim
  2. Thêm vào Wishlist
  3. Có thể xem lại sau

### UC15: Đánh giá sản phẩm
- **Actor:** Khách hàng (đã mua)
- **Mô tả:** Viết review cho sản phẩm
- **Luồng chính:**
  1. Vào trang sản phẩm đã mua
  2. Chọn số sao (1-5)
  3. Viết tiêu đề, nội dung
  4. Submit
  5. Admin duyệt

### UC16: Đánh giá cửa hàng
- **Actor:** Khách hàng (đã mua)
- **Mô tả:** Đánh giá tổng thể cửa hàng
- **Luồng chính:**
  1. Vào trang đánh giá
  2. Chọn số sao
  3. Viết nội dung
  4. Submit (1 lần/user)

### UC17: Đăng ký nhận tin
- **Actor:** Khách hàng
- **Mô tả:** Đăng ký Newsletter
- **Luồng chính:**
  1. Nhập email vào form
  2. Xác nhận đăng ký
  3. Nhận tin khuyến mãi

### UC18: Thêm/Sửa/Xóa sản phẩm
- **Actor:** Admin
- **Mô tả:** CRUD sản phẩm
- **Luồng chính:**
  1. Vào trang quản lý sản phẩm
  2. Thêm mới:
     - Nhập thông tin đầy đủ
     - Upload ảnh chính + gallery
     - Chọn danh mục
     - Đặt giá, tồn kho
  3. Sửa/Xóa sản phẩm hiện có

### UC19: Quản lý danh mục
- **Actor:** Admin
- **Mô tả:** CRUD danh mục
- **Luồng chính:**
  1. Thêm/Sửa/Xóa category
  2. Upload ảnh danh mục
  3. Xem số lượng sản phẩm
  4. Xem doanh thu theo danh mục

### UC20: Quản lý đánh giá
- **Actor:** Admin
- **Mô tả:** Kiểm duyệt review
- **Luồng chính:**
  1. Xem danh sách đánh giá
  2. Duyệt/Ẩn review
  3. Xóa spam
  4. Đặt review nổi bật

---

## 📦 PACKAGE 3: GIỎ HÀNG & ĐẶT HÀNG (10 Use Cases)

### UC30: Thêm vào giỏ hàng
- **Actor:** Khách hàng (không cần login)
- **Mô tả:** Thêm sản phẩm vào cart
- **Luồng chính:**
  1. Chọn số lượng
  2. Click "Thêm vào giỏ"
  3. Kiểm tra tồn kho
  4. Lưu vào session
  5. Cập nhật badge giỏ hàng
- **Luồng ngoại lệ:**
  - Hết hàng → Thông báo lỗi
  - Vượt quá tồn kho → Giảm xuống max

### UC31: Xem giỏ hàng
- **Actor:** Khách hàng
- **Mô tả:** Xem cart
- **Luồng chính:**
  1. Vào trang giỏ hàng
  2. Hiển thị:
     - Danh sách sản phẩm
     - Ảnh, Tên, Giá, Số lượng
     - Tạm tính
     - Phí ship (ước tính)
  3. Nút "Thanh toán"

### UC32: Cập nhật giỏ hàng
- **Actor:** Khách hàng
- **Mô tả:** Thay đổi số lượng
- **Luồng chính:**
  1. Tăng/Giảm số lượng
  2. Kiểm tra tồn kho
  3. Cập nhật tổng tiền

### UC33: Xóa sản phẩm khỏi giỏ
- **Actor:** Khách hàng
- **Mô tả:** Xóa item
- **Luồng chính:**
  1. Click nút xóa
  2. Xác nhận
  3. Cập nhật giỏ hàng

### UC34: Thanh toán (Checkout)
- **Actor:** Khách hàng (phải login)
- **Mô tả:** Hoàn tất đơn hàng
- **Luồng chính:**
  1. Nhập địa chỉ giao hàng
  2. Nhập SĐT, Email
  3. Chọn khu vực → Tính phí ship
  4. Áp dụng mã giảm giá (UC35)
  5. Chọn phương thức thanh toán (UC36)
  6. Xác nhận đơn hàng (UC39)
  7. Tạo Order với status = Pending
  8. Gửi email xác nhận (UC100)

### UC35: Áp dụng mã giảm giá
- **Actor:** Khách hàng
- **Mô tả:** Dùng discount code
- **Luồng chính:**
  1. Nhập mã giảm giá
  2. Kiểm tra:
     - Còn hiệu lực?
     - Đủ điều kiện đơn tối thiểu?
     - Còn lượt sử dụng?
  3. Áp dụng và tính lại tổng
- **Luồng ngoại lệ:**
  - Mã không hợp lệ → Thông báo

### UC36: Chọn phương thức thanh toán
- **Actor:** Khách hàng
- **Mô tả:** Chọn payment method
- **Các lựa chọn:**
  - COD (Thanh toán khi nhận hàng) → UC38
  - VNPay (Thanh toán online) → UC37
  - Chuyển khoản ngân hàng
  - Thẻ tín dụng
  - Ví điện tử

### UC37: Thanh toán VNPay
- **Actor:** Khách hàng, VNPay
- **Mô tả:** Thanh toán qua VNPay
- **Luồng chính:**
  1. Chuyển đến VNPay gateway
  2. Chọn ngân hàng
  3. Đăng nhập internet banking
  4. Xác nhận thanh toán
  5. VNPay callback về hệ thống
  6. Cập nhật payment_status = Paid
  7. Gửi email xác nhận (UC100)

### UC38: Thanh toán COD
- **Actor:** Khách hàng
- **Mô tả:** Thanh toán khi nhận hàng
- **Luồng chính:**
  1. Chọn COD
  2. Xác nhận đơn
  3. Payment_status = Pending
  4. Shipper thu tiền khi giao

### UC39: Xác nhận đơn hàng
- **Actor:** Khách hàng
- **Mô tả:** Hoàn tất checkout
- **Luồng chính:**
  1. Review lại đơn hàng
  2. Xác nhận
  3. Tạo Order
  4. Trừ tồn kho
  5. Tăng used_count của mã giảm giá
  6. Xóa giỏ hàng
  7. Gửi email (UC100)
  8. Chuyển đến trang "Cảm ơn"

---

## 📦 PACKAGE 4: QUẢN LÝ ĐƠN HÀNG (8 Use Cases)

### UC50: Xem lịch sử đơn hàng
- **Actor:** Khách hàng
- **Mô tả:** Xem các đơn đã đặt
- **Luồng chính:**
  1. Vào trang "Đơn hàng của tôi"
  2. Hiển thị danh sách orders
  3. Thông tin: Mã đơn, Ngày, Tổng tiền, Trạng thái

### UC51: Xem chi tiết đơn hàng
- **Actor:** Khách hàng
- **Mô tả:** Xem thông tin đầy đủ
- **Luồng chính:**
  1. Click vào đơn hàng
  2. Hiển thị:
     - Danh sách sản phẩm
     - Địa chỉ giao hàng
     - Phương thức thanh toán
     - Trạng thái
     - Timeline tracking

### UC52: Theo dõi trạng thái đơn
- **Actor:** Khách hàng
- **Mô tả:** Xem tiến trình xử lý
- **Luồng chính:**
  1. Xem timeline:
     - Pending → Confirmed → Processing → Shipped → Delivered
  2. Xem thời gian mỗi bước
  3. Xem thông tin shipper (nếu có)

### UC53: Hủy đơn hàng
- **Actor:** Khách hàng
- **Mô tả:** Hủy đơn chưa xử lý
- **Điều kiện:** Status = Pending hoặc Confirmed
- **Luồng chính:**
  1. Click "Hủy đơn"
  2. Nhập lý do
  3. Xác nhận
  4. Cập nhật status = Canceled
  5. Hoàn lại tồn kho
  6. Hoàn tiền (nếu đã thanh toán)

### UC54: Quản lý đơn hàng (Admin)
- **Actor:** Admin
- **Mô tả:** Xem tất cả đơn hàng
- **Luồng chính:**
  1. Vào trang quản lý orders
  2. Hiển thị danh sách (phân trang)
  3. Tìm kiếm theo: Mã đơn, SĐT, Email
  4. Lọc theo: Trạng thái, Thanh toán, Ngày
  5. Xem chi tiết
  6. Cập nhật trạng thái

### UC55: Cập nhật trạng thái đơn
- **Actor:** Admin
- **Mô tả:** Chuyển trạng thái
- **Luồng chính:**
  1. Chọn đơn hàng
  2. Chọn trạng thái mới
  3. Nhập ghi chú (tùy chọn)
  4. Xác nhận
  5. Tạo OrderTracking log
  6. Gửi email thông báo (UC101)

### UC56: Xem báo cáo đơn hàng
- **Actor:** Admin
- **Mô tả:** Thống kê orders
- **Luồng chính:**
  1. Chọn khoảng thời gian
  2. Xem:
     - Tổng đơn hàng
     - Doanh thu
     - Đơn trung bình
     - Phân bố trạng thái
     - Top khách hàng

### UC57: Quản lý mã giảm giá
- **Actor:** Admin
- **Mô tả:** CRUD discount codes
- **Luồng chính:**
  1. Thêm mã mới:
     - Code
     - Loại (%, fixed)
     - Giá trị
     - Đơn tối thiểu
     - Số lần sử dụng
     - Thời gian hiệu lực
  2. Bật/Tắt mã
  3. Xem thống kê sử dụng

---

## 📦 PACKAGE 5: QUẢN LÝ GIAO HÀNG (10 Use Cases)

### UC70: Phân công shipper
- **Actor:** Admin
- **Mô tả:** Gán đơn cho shipper
- **Luồng chính:**
  1. Chọn đơn hàng (status = Processing)
  2. Chọn shipper available
  3. Nhập thời gian dự kiến
  4. Xác nhận
  5. Tạo Delivery record (status = Assigned)
  6. Gửi email cho shipper (UC102)
  7. Cập nhật Order status = Shipped

### UC71: Xem đơn được phân công
- **Actor:** Shipper
- **Mô tả:** Xem danh sách delivery
- **Luồng chính:**
  1. Login với role = shipper
  2. Vào trang "Đơn của tôi"
  3. Hiển thị:
     - Đơn đang giao
     - Đơn đã giao
     - Thống kê cá nhân

### UC72: Xác nhận lấy hàng
- **Actor:** Shipper
- **Mô tả:** Đã nhận hàng từ kho
- **Luồng chính:**
  1. Xem chi tiết đơn
  2. Click "Đã lấy hàng"
  3. Xác nhận
  4. Cập nhật Delivery status = Picked Up
  5. Tạo DeliveryTracking log

### UC73: Cập nhật trạng thái giao hàng
- **Actor:** Shipper
- **Mô tả:** Cập nhật tiến trình
- **Luồng chính:**
  1. Chọn trạng thái:
     - In Transit (Đang giao)
     - Delivered (Đã giao)
     - Failed (Thất bại)
  2. Nhập ghi chú
  3. Upload ảnh (nếu giao thành công)
  4. Xác nhận
  5. Tạo tracking log
  6. Cập nhật real-time (UC76)

### UC74: Upload ảnh giao hàng
- **Actor:** Shipper
- **Mô tả:** Chứng minh đã giao
- **Luồng chính:**
  1. Chụp ảnh hàng đã giao
  2. Upload vào hệ thống
  3. Lưu vào Delivery.proof_image

### UC75: Báo giao thất bại
- **Actor:** Shipper
- **Mô tả:** Không giao được hàng
- **Luồng chính:**
  1. Chọn "Giao thất bại"
  2. Chọn lý do:
     - Khách không nhận máy
     - Địa chỉ sai
     - Khách từ chối nhận
     - Lý do khác
  3. Nhập ghi chú chi tiết
  4. Xác nhận
  5. Delivery status = Failed
  6. Admin xử lý tiếp

### UC76: Theo dõi giao hàng (Real-time)
- **Actor:** Khách hàng, Admin
- **Mô tả:** Xem vị trí shipper
- **Luồng chính:**
  1. Vào trang tracking
  2. Hiển thị:
     - Vị trí hiện tại (GPS)
     - Timeline delivery
     - Thông tin shipper
     - SĐT liên hệ
  3. Real-time updates

### UC77: Quản lý shipper
- **Actor:** Admin
- **Mô tả:** CRUD shipper accounts
- **Luồng chính:**
  1. Thêm shipper mới:
     - Tạo User account
     - Tạo DeliveryPerson profile
     - Nhập SĐT, phương tiện, biển số
  2. Bật/Tắt shipper
  3. Xem hiệu suất

### UC78: Xem thống kê shipper
- **Actor:** Admin
- **Mô tả:** Đánh giá hiệu suất
- **Luồng chính:**
  1. Xem từng shipper:
     - Tổng đơn đã giao
     - Đơn thành công
     - Tỷ lệ thành công
     - Đánh giá trung bình
     - Đơn đang giao
  2. So sánh giữa các shipper
  3. Top performer

### UC79: Quản lý khu vực giao hàng
- **Actor:** Admin
- **Mô tả:** Cấu hình delivery zones
- **Luồng chính:**
  1. Thêm khu vực mới:
     - Tên khu vực
     - Danh sách quận/huyện
     - Phí ship cơ bản
     - Phí mỗi km
     - Thời gian dự kiến
  2. Sửa/Xóa khu vực
  3. Bật/Tắt khu vực

---

## 📦 PACKAGE 6: BÁO CÁO & THỐNG KÊ (8 Use Cases)

### UC90: Xem dashboard tổng quan
- **Actor:** Admin
- **Mô tả:** Dashboard chính
- **Luồng chính:**
  1. Vào trang dashboard
  2. Hiển thị:
     - **Cards thống kê:**
       - Tổng doanh thu
       - Doanh thu tháng
       - Tăng trưởng %
       - Tổng đơn hàng
       - Đơn chờ xử lý
       - Tổng khách hàng
       - Khách mới tháng
       - Tổng sản phẩm
     - **Biểu đồ:**
       - Doanh thu 12 tháng (line chart)
       - Doanh thu 30 ngày (bar chart)
       - Trạng thái đơn hàng (pie chart)
       - Top sản phẩm (bar chart)
     - **Bảng:**
       - 10 đơn hàng mới nhất
       - Top 5 sản phẩm bán chạy
       - 5 sản phẩm tồn kho thấp
       - 5 đánh giá mới nhất
       - Top 5 shipper

### UC91: Xem báo cáo doanh thu
- **Actor:** Admin
- **Mô tả:** Phân tích revenue
- **Luồng chính:**
  1. Chọn khoảng thời gian
  2. Xem:
     - Doanh thu theo ngày
     - Tổng doanh thu
     - Doanh thu trung bình/đơn
     - Biểu đồ xu hướng
     - So sánh với kỳ trước

### UC92: Xem thống kê sản phẩm
- **Actor:** Admin
- **Mô tả:** Phân tích products
- **Luồng chính:**
  1. Xem:
     - Top bán chạy
     - Sản phẩm theo doanh thu
     - Tồn kho thấp
     - Sản phẩm chưa bán
     - Đánh giá cao nhất
  2. Lọc theo danh mục, thời gian

### UC93: Xem thống kê khách hàng
- **Actor:** Admin
- **Mô tả:** Phân tích customers
- **Luồng chính:**
  1. Xem:
     - Tổng khách hàng
     - Khách mới theo thời gian
     - Top khách hàng (theo chi tiêu)
     - Tỷ lệ khách quay lại
     - Phân bố địa lý

### UC94: Xem biểu đồ phân tích
- **Actor:** Admin
- **Mô tả:** Visualize data
- **Các loại biểu đồ:**
  - Line chart: Doanh thu theo thời gian
  - Bar chart: So sánh sản phẩm, danh mục
  - Pie chart: Phân bố trạng thái, payment method
  - Area chart: Xu hướng
  - Heatmap: Đơn hàng theo giờ/ngày

### UC95: Export báo cáo CSV
- **Actor:** Admin
- **Mô tả:** Xuất dữ liệu
- **Luồng chính:**
  1. Chọn loại báo cáo:
     - Báo cáo đơn hàng
     - Báo cáo sản phẩm
     - Báo cáo khách hàng
     - Báo cáo doanh thu
  2. Chọn khoảng thời gian
  3. Click "Export CSV"
  4. Download file (UTF-8 with BOM)

### UC96: Quản lý user (All roles)
- **Actor:** Admin
- **Mô tả:** CRUD tất cả users
- **Luồng chính:**
  1. Xem danh sách users
  2. Lọc theo role: admin, customer, shipper
  3. Thêm/Sửa/Xóa user
  4. Phân quyền (groups)
  5. Bật/Tắt tài khoản
  6. Reset password

### UC97: Quản lý Newsletter
- **Actor:** Admin
- **Mô tả:** Quản lý subscribers
- **Luồng chính:**
  1. Xem danh sách email đăng ký
  2. Lọc theo trạng thái (active/inactive)
  3. Gửi email hàng loạt
  4. Xóa email
  5. Xem thống kê đăng ký mới

---

## 📦 PACKAGE 7: HỆ THỐNG THÔNG BÁO (4 Use Cases)

### UC100: Gửi email xác nhận đơn
- **Actor:** Hệ thống Email
- **Trigger:** Sau khi tạo Order thành công
- **Nội dung email:**
  - Mã đơn hàng
  - Danh sách sản phẩm
  - Tổng tiền
  - Địa chỉ giao hàng
  - Phương thức thanh toán
  - Link theo dõi đơn

### UC101: Gửi email cập nhật trạng thái
- **Actor:** Hệ thống Email
- **Trigger:** Admin cập nhật trạng thái đơn
- **Nội dung email:**
  - Mã đơn hàng
  - Trạng thái mới
  - Thời gian cập nhật
  - Ghi chú (nếu có)
  - Thông tin shipper (nếu đã giao)

### UC102: Gửi email phân công shipper
- **Actor:** Hệ thống Email
- **Trigger:** Admin phân công đơn cho shipper
- **Nội dung email:**
  - Thông tin đơn hàng
  - Địa chỉ lấy hàng
  - Địa chỉ giao hàng
  - Tên người nhận, SĐT
  - Thời gian dự kiến
  - Link xem chi tiết

### UC103: Gửi email Newsletter
- **Actor:** Hệ thống Email
- **Trigger:** Admin gửi tin tức/khuyến mãi
- **Nội dung email:**
  - Thông báo sản phẩm mới
  - Khuyến mãi, mã giảm giá
  - Tin tức cửa hàng
  - Link unsubscribe

---

## 🔗 QUAN HỆ GIỮA CÁC USE CASE

### Include Relationships (<<include>>)
- **UC34** (Thanh toán) include:
  - UC35 (Áp dụng mã giảm giá)
  - UC36 (Chọn phương thức thanh toán)
  - UC39 (Xác nhận đơn hàng)

- **UC37** (Thanh toán VNPay) include:
  - UC100 (Gửi email xác nhận)

- **UC39** (Xác nhận đơn) include:
  - UC100 (Gửi email xác nhận)

- **UC55** (Cập nhật trạng thái) include:
  - UC101 (Gửi email cập nhật)

- **UC70** (Phân công shipper) include:
  - UC102 (Gửi email shipper)

- **UC73** (Cập nhật giao hàng) include:
  - UC76 (Real-time tracking)

### Extend Relationships (<<extend>>)
- **UC36** (Chọn payment) extend:
  - UC37 (VNPay)
  - UC38 (COD)

- **UC15** (Đánh giá sản phẩm) extend UC12 (Xem chi tiết)
- **UC16** (Đánh giá shop) extend UC50 (Lịch sử đơn)
- **UC30** (Thêm giỏ) extend UC10/UC12
- **UC53** (Hủy đơn) extend UC51 (Chi tiết đơn)

---

## 📊 THỐNG KÊ USE CASE THEO ACTOR

| Actor | Số Use Cases | Chức năng chính |
|-------|--------------|-----------------|
| **Khách hàng** | 24 | Mua sắm, Đặt hàng, Theo dõi |
| **Admin** | 20 | Quản lý toàn bộ hệ thống |
| **Shipper** | 6 | Giao hàng, Cập nhật |
| **VNPay** | 2 | Xử lý thanh toán |
| **Email** | 4 | Gửi thông báo |

---

## 🎯 CÁC USE CASE QUAN TRỌNG NHẤT

### Top 10 Use Cases cốt lõi:
1. **UC34** - Thanh toán (Checkout) ⭐⭐⭐⭐⭐
2. **UC12** - Xem chi tiết sản phẩm ⭐⭐⭐⭐⭐
3. **UC54** - Quản lý đơn hàng (Admin) ⭐⭐⭐⭐⭐
4. **UC70** - Phân công shipper ⭐⭐⭐⭐
5. **UC73** - Cập nhật giao hàng ⭐⭐⭐⭐
6. **UC90** - Dashboard tổng quan ⭐⭐⭐⭐
7. **UC37** - Thanh toán VNPay ⭐⭐⭐⭐
8. **UC18** - Quản lý sản phẩm ⭐⭐⭐
9. **UC15** - Đánh giá sản phẩm ⭐⭐⭐
10. **UC91** - Báo cáo doanh thu ⭐⭐⭐

---

## 💡 LƯU Ý THIẾT KẾ

1. **Session-based Cart**: Không cần login để thêm vào giỏ
2. **VNPay Sandbox**: Test môi trường thanh toán
3. **Email SMTP**: Tự động gửi thông báo
4. **Real-time Tracking**: Chuẩn bị cho GPS tracking
5. **Role-based Access**: Admin, Customer, Shipper
6. **Order Workflow**: 7 trạng thái rõ ràng
7. **Delivery Workflow**: 6 trạng thái giao hàng
8. **Dashboard Analytics**: Biểu đồ và thống kê đầy đủ

---

**Tổng kết:** Hệ thống có **46+ Use Cases** phục vụ **4 Actor chính**, bao quát đầy đủ quy trình mua bán trái cây trực tuyến từ A-Z.


