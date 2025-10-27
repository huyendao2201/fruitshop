# 📊 TÓM TẮT USE CASE DIAGRAM - FRESHBERRY FRUIT SHOP

## 🎯 THỐNG KÊ TỔNG QUAN

| Chỉ số | Số lượng |
|--------|----------|
| **Tổng Use Cases** | **46+** |
| **Actors** | **4** (Khách hàng, Admin, Shipper, Hệ thống) |
| **Packages** | **7** (Modules chức năng) |
| **Apps Django** | **5** (accounts, products, orders, delivery, reports) |

---

## 🎭 ACTORS VÀ PHÂN BỔ USE CASES

### 1. 👤 Khách hàng (Customer) - 24 Use Cases

#### Quản lý tài khoản (6)
- UC1: Đăng ký tài khoản
- UC2: Đăng nhập
- UC3: Đăng xuất
- UC4: Xem thông tin cá nhân
- UC5: Cập nhật thông tin
- UC6: Quản lý địa chỉ

#### Sản phẩm (7)
- UC10: Xem danh sách sản phẩm
- UC11: Tìm kiếm sản phẩm
- UC12: Xem chi tiết sản phẩm ⭐
- UC13: Lọc theo danh mục
- UC14: Thêm vào yêu thích
- UC15: Đánh giá sản phẩm
- UC16: Đánh giá cửa hàng
- UC17: Đăng ký nhận tin

#### Mua sắm (7)
- UC30: Thêm vào giỏ hàng
- UC31: Xem giỏ hàng
- UC32: Cập nhật giỏ hàng
- UC33: Xóa sản phẩm khỏi giỏ
- UC34: Thanh toán (Checkout) ⭐⭐⭐
- UC35: Áp dụng mã giảm giá
- UC39: Xác nhận đơn hàng

#### Đơn hàng (4)
- UC50: Xem lịch sử đơn hàng
- UC51: Xem chi tiết đơn hàng
- UC52: Theo dõi trạng thái đơn
- UC53: Hủy đơn hàng
- UC76: Theo dõi giao hàng (Real-time) ⭐

---

### 2. 👨‍💼 Admin (Quản trị viên) - 20 Use Cases

#### Quản lý sản phẩm (3)
- UC18: Thêm/Sửa/Xóa sản phẩm ⭐
- UC19: Quản lý danh mục
- UC20: Quản lý đánh giá

#### Quản lý đơn hàng (4)
- UC54: Quản lý đơn hàng (Admin) ⭐⭐⭐
- UC55: Cập nhật trạng thái đơn ⭐
- UC56: Xem báo cáo đơn hàng
- UC57: Quản lý mã giảm giá

#### Quản lý giao hàng (4)
- UC70: Phân công shipper ⭐⭐⭐
- UC77: Quản lý shipper
- UC78: Xem thống kê shipper
- UC79: Quản lý khu vực giao hàng

#### Báo cáo & Thống kê (8)
- UC90: Xem dashboard tổng quan ⭐⭐⭐
- UC91: Xem báo cáo doanh thu ⭐⭐
- UC92: Xem thống kê sản phẩm
- UC93: Xem thống kê khách hàng
- UC94: Xem biểu đồ phân tích
- UC95: Export báo cáo CSV
- UC96: Quản lý user (All roles)
- UC97: Quản lý Newsletter

#### Khác (1)
- UC2: Đăng nhập (Admin)
- UC3: Đăng xuất

---

### 3. 🚚 Shipper (Nhân viên giao hàng) - 6 Use Cases

- UC2: Đăng nhập
- UC3: Đăng xuất
- UC71: Xem đơn được phân công ⭐
- UC72: Xác nhận lấy hàng ⭐
- UC73: Cập nhật trạng thái giao hàng ⭐⭐
- UC74: Upload ảnh giao hàng
- UC75: Báo giao thất bại

---

### 4. 🔧 Hệ thống bên ngoài - 6 Use Cases

#### VNPay (2)
- UC37: Thanh toán VNPay ⭐⭐
- UC38: Thanh toán COD

#### Email (4)
- UC100: Gửi email xác nhận đơn
- UC101: Gửi email cập nhật trạng thái
- UC102: Gửi email phân công shipper
- UC103: Gửi email Newsletter

---

## 📦 7 PACKAGES (MODULES CHỨC NĂNG)

### Package 1: Quản lý Tài khoản
**Tổng:** 6 Use Cases  
**Apps:** `accounts`  
**Chức năng:** Đăng ký, đăng nhập, profile, địa chỉ giao hàng

### Package 2: Quản lý Sản phẩm
**Tổng:** 11 Use Cases  
**Apps:** `products`  
**Chức năng:** CRUD sản phẩm, danh mục, review, wishlist, mã giảm giá, newsletter

### Package 3: Giỏ hàng & Đặt hàng
**Tổng:** 10 Use Cases  
**Apps:** `orders`  
**Chức năng:** Session cart, checkout, thanh toán VNPay/COD, áp mã giảm giá

### Package 4: Quản lý Đơn hàng
**Tổng:** 8 Use Cases  
**Apps:** `orders`  
**Chức năng:** Xem/hủy đơn, tracking, quản lý trạng thái, báo cáo

### Package 5: Quản lý Giao hàng
**Tổng:** 10 Use Cases  
**Apps:** `delivery`  
**Chức năng:** Phân công shipper, tracking real-time, delivery workflow, thống kê

### Package 6: Báo cáo & Thống kê
**Tổng:** 8 Use Cases  
**Apps:** `reports`  
**Chức năng:** Dashboard, analytics, biểu đồ, export CSV, quản lý users

### Package 7: Hệ thống Thông báo
**Tổng:** 4 Use Cases  
**Apps:** Tích hợp trong các apps khác  
**Chức năng:** Email automation (SMTP Gmail)

---

## 🔗 QUAN HỆ GIỮA USE CASES

### Include (<<include>>) - Bắt buộc
```
UC34 (Thanh toán) INCLUDE:
  ├── UC35 (Áp dụng mã giảm giá)
  ├── UC36 (Chọn phương thức thanh toán)
  └── UC39 (Xác nhận đơn hàng)

UC37 (VNPay) INCLUDE:
  └── UC100 (Gửi email)

UC55 (Cập nhật trạng thái) INCLUDE:
  └── UC101 (Gửi email)

UC70 (Phân công shipper) INCLUDE:
  └── UC102 (Gửi email)

UC73 (Cập nhật giao hàng) INCLUDE:
  └── UC76 (Real-time tracking)
```

### Extend (<<extend>>) - Tùy chọn
```
UC36 (Chọn payment) EXTEND:
  ├── UC37 (VNPay)
  └── UC38 (COD)

UC12 (Chi tiết sản phẩm) EXTEND:
  └── UC15 (Đánh giá)

UC50 (Lịch sử đơn) EXTEND:
  └── UC16 (Đánh giá shop)

UC10/UC12 (Sản phẩm) EXTEND:
  └── UC30 (Thêm giỏ)

UC51 (Chi tiết đơn) EXTEND:
  └── UC53 (Hủy đơn)
```

---

## ⭐ TOP 10 USE CASES QUAN TRỌNG NHẤT

| # | Use Case | Độ quan trọng | Lý do |
|---|----------|---------------|-------|
| 1 | UC34 - Thanh toán | ⭐⭐⭐⭐⭐ | Core business flow |
| 2 | UC12 - Chi tiết sản phẩm | ⭐⭐⭐⭐⭐ | Thông tin đầy đủ trước mua |
| 3 | UC54 - Quản lý đơn (Admin) | ⭐⭐⭐⭐⭐ | Nghiệp vụ chính Admin |
| 4 | UC70 - Phân công shipper | ⭐⭐⭐⭐ | Delivery workflow |
| 5 | UC73 - Cập nhật giao hàng | ⭐⭐⭐⭐ | Real-time tracking |
| 6 | UC90 - Dashboard | ⭐⭐⭐⭐ | Admin analytics |
| 7 | UC37 - VNPay | ⭐⭐⭐⭐ | Online payment |
| 8 | UC18 - Quản lý sản phẩm | ⭐⭐⭐ | CRUD sản phẩm |
| 9 | UC15 - Đánh giá | ⭐⭐⭐ | Social proof |
| 10 | UC91 - Báo cáo doanh thu | ⭐⭐⭐ | Business analytics |

---

## 🔄 QUY TRÌNH NGHIỆP VỤ CHÍNH

### 1️⃣ Quy trình Mua hàng (Customer Journey)
```
UC10/UC11 (Duyệt sản phẩm)
    ↓
UC12 (Xem chi tiết)
    ↓
UC30 (Thêm vào giỏ)
    ↓
UC31 (Xem giỏ hàng)
    ↓
UC2 (Đăng nhập - nếu chưa)
    ↓
UC34 (Checkout)
    ├── UC35 (Áp mã giảm giá)
    ├── UC36 → UC37/UC38 (Chọn payment)
    └── UC39 (Xác nhận đơn)
    ↓
UC100 (Nhận email xác nhận)
    ↓
UC52/UC76 (Theo dõi đơn)
    ↓
UC15/UC16 (Đánh giá)
```

### 2️⃣ Quy trình Xử lý đơn hàng (Admin Workflow)
```
UC54 (Nhận đơn mới - Pending)
    ↓
UC55 (Xác nhận đơn - Confirmed)
    ↓
UC55 (Chuẩn bị hàng - Processing)
    ↓
UC70 (Phân công shipper)
    ├── UC102 (Gửi email cho shipper)
    └── UC55 (Cập nhật → Shipped)
```

### 3️⃣ Quy trình Giao hàng (Shipper Workflow)
```
UC102 (Nhận email phân công)
    ↓
UC71 (Xem đơn được giao)
    ↓
UC72 (Xác nhận lấy hàng - Picked Up)
    ↓
UC73 (Đang giao - In Transit)
    └── UC76 (Real-time tracking)
    ↓
[Giao thành công]
    ├── UC74 (Upload ảnh chứng minh)
    └── UC73 (Cập nhật → Delivered)
HOẶC
[Giao thất bại]
    └── UC75 (Báo thất bại + lý do)
```

---

## 🎨 MÀU SẮC PHÂN BIỆT TRONG SƠ ĐỒ

- **Customer** - Xanh dương (#LightBlue)
- **Admin** - Cam (#Orange)
- **Shipper** - Xanh lá (#LightGreen)
- **VNPay** - Vàng (#Yellow)
- **Email** - Hồng (#Pink)

---

## 📁 CẤU TRÚC FILE TÀI LIỆU

```
docs/
├── README.md                         # Hướng dẫn chung
├── USE-CASE-SUMMARY.md              # File này - Tóm tắt nhanh
├── use-case-description.md          # Mô tả chi tiết 46+ UCs
├── use-case-diagram.puml            # Sơ đồ đầy đủ (PlantUML)
├── use-case-diagram-simple.puml     # Sơ đồ đơn giản
└── view-diagram.html                # Web viewer (mở bằng browser)
```

---

## 🚀 CÁCH SỬ DỤNG TÀI LIỆU

### Cho Sinh viên / Người học:
1. Đọc file này để hiểu tổng quan
2. Xem sơ đồ bằng PlantUML online viewer
3. Đọc `use-case-description.md` để hiểu chi tiết từng UC

### Cho Giảng viên / Đánh giá:
1. Mở `view-diagram.html` trong browser
2. Xem sơ đồ qua PlantUML viewer
3. Kiểm tra tính đầy đủ của 46+ use cases

### Cho Developers:
1. Cài PlantUML extension trong VS Code/IntelliJ
2. Mở file `.puml` để xem và chỉnh sửa
3. Export PNG/SVG cho documentation

---

## 🔍 XEM SƠ ĐỒ NHANH

**Online (Không cần cài đặt):**
1. Copy nội dung file `use-case-diagram.puml`
2. Paste vào: http://www.plantuml.com/plantuml/uml/
3. Xem và download

**Hoặc mở file `view-diagram.html` trong browser để xem hướng dẫn đầy đủ.**

---

## ✅ CHECKLIST ĐÁNH GIÁ USE CASE DIAGRAM

- [x] Xác định đầy đủ actors (4 actors)
- [x] Định nghĩa 46+ use cases
- [x] Nhóm thành packages logic (7 packages)
- [x] Xác định quan hệ Include
- [x] Xác định quan hệ Extend
- [x] Vẽ sơ đồ bằng công cụ chuẩn (PlantUML)
- [x] Mô tả chi tiết từng use case
- [x] Xác định luồng chính và phụ
- [x] Phân tích quy trình nghiệp vụ
- [x] Tài liệu hóa đầy đủ

---

## 📞 THÔNG TIN LIÊN HỆ

**Project:** FreshBerry Fruit Shop  
**Tech Stack:** Django 5.2+, MySQL, VNPay, Gmail SMTP  
**Version:** 1.0  
**Last Updated:** 2025-10-26

---

**Ghi chú:** Đây là tài liệu thiết kế use case hoàn chỉnh dựa trên phân tích hệ thống thực tế. Sơ đồ và mô tả có thể được mở rộng khi thêm tính năng mới.


