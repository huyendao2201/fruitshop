# TÀI LIỆU THIẾT KẾ - FRESHBERRY FRUIT SHOP

## 📁 Cấu trúc thư mục

```
docs/
├── README.md                      # File này - Hướng dẫn
├── use-case-diagram.puml          # Sơ đồ Use Case (PlantUML)
└── use-case-description.md        # Mô tả chi tiết 46+ Use Cases
```

---

## 🎨 Xem sơ đồ Use Case Diagram

File `use-case-diagram.puml` được viết bằng **PlantUML** - ngôn ngữ mô tả sơ đồ UML chuẩn.

### 📐 Layout Vertical (Dọc) ⭐
Tất cả sơ đồ đã được thiết lập **vertical layout (top to bottom)** để:
- ✅ Dễ đọc hơn (theo thói quen từ trên xuống)
- ✅ In ấn tốt trên giấy A4 dọc
- ✅ Phù hợp với presentation
- ✅ Workflow logic rõ ràng

### Cách 1: Xem trực tuyến (Nhanh nhất)
1. Mở file `use-case-diagram.puml`
2. Copy toàn bộ nội dung
3. Vào trang: http://www.plantuml.com/plantuml/uml/
4. Paste vào và xem kết quả
5. Có thể download dạng PNG, SVG, PDF

### Cách 2: Sử dụng VS Code Extension
1. Cài extension: **PlantUML** (tác giả: jebbs)
2. Mở file `use-case-diagram.puml`
3. Nhấn `Alt + D` để xem preview
4. Hoặc chuột phải → "Preview Current Diagram"

**Yêu cầu:**
- Cài Java (JRE/JDK)
- Extension sẽ tự động tải PlantUML

### Cách 3: Sử dụng IntelliJ IDEA / PyCharm
1. Cài plugin: **PlantUML Integration**
2. Mở file `.puml`
3. Sơ đồ tự động hiển thị bên cạnh

### Cách 4: Command Line (Local)
```bash
# Cài PlantUML
npm install -g node-plantuml

# Render thành PNG
puml generate docs/use-case-diagram.puml -o docs/use-case-diagram.png

# Hoặc dùng Java
java -jar plantuml.jar docs/use-case-diagram.puml
```

### Cách 5: Online Editor khác
- https://plantuml-editor.kkeisuke.com/
- https://liveuml.com/
- https://www.planttext.com/

---

## 📊 Nội dung sơ đồ Use Case

Sơ đồ bao gồm:

### 🎭 Actors (4 loại):
1. **Khách hàng (Customer)** - 24 use cases
2. **Quản trị viên (Admin)** - 20 use cases
3. **Nhân viên giao hàng (Shipper)** - 6 use cases
4. **Hệ thống bên ngoài:**
   - VNPay - Thanh toán
   - Email - Thông báo

### 📦 Packages (7 modules):
1. **Quản lý Tài khoản** (6 UCs)
   - Đăng ký, Đăng nhập, Profile, Địa chỉ

2. **Quản lý Sản phẩm** (11 UCs)
   - CRUD sản phẩm, Danh mục, Đánh giá, Wishlist

3. **Giỏ hàng & Đặt hàng** (10 UCs)
   - Cart, Checkout, Payment (VNPay/COD), Mã giảm giá

4. **Quản lý Đơn hàng** (8 UCs)
   - Xem/Hủy đơn, Cập nhật trạng thái, Báo cáo

5. **Quản lý Giao hàng** (10 UCs)
   - Phân công, Tracking, Shipper management

6. **Báo cáo & Thống kê** (8 UCs)
   - Dashboard, Analytics, Export CSV

7. **Hệ thống Thông báo** (4 UCs)
   - Email automation

### 🔗 Relationships:
- **Include** (<<include>>): Use case bắt buộc
  - VD: Thanh toán INCLUDE Áp mã giảm giá
  
- **Extend** (<<extend>>): Use case tùy chọn
  - VD: Chọn payment EXTEND VNPay hoặc COD

### 📝 Notes:
- Giỏ hàng không cần login
- VNPay sử dụng Sandbox
- Shipper nhận email khi phân công
- Dashboard có biểu đồ và thống kê

---

## 📖 Mô tả chi tiết Use Cases

Xem file `use-case-description.md` để đọc:
- Mô tả đầy đủ 46+ use cases
- Luồng chính (Main flow)
- Luồng ngoại lệ (Alternative flow)
- Điều kiện tiên quyết
- Kết quả mong đợi
- Quan hệ giữa các use case

---

## 🖼️ Preview sơ đồ

Sơ đồ Use Case bao gồm:
- 4 Actors với icon đẹp
- 7 Packages được nhóm rõ ràng
- 46+ Use Cases được sắp xếp logic
- Các mối quan hệ (Association, Include, Extend)
- Notes giải thích
- Styling chuyên nghiệp

**Kích thước:** Khoảng 1200x1600 pixels (A4 portrait)

---

## 📚 Tài liệu khác (nếu cần bổ sung)

### Các sơ đồ có thể thêm:
- [ ] Class Diagram (Sơ đồ lớp)
- [ ] Sequence Diagram (Sơ đồ tuần tự)
- [ ] Activity Diagram (Sơ đồ hoạt động)
- [ ] ER Diagram (Sơ đồ CSDL)
- [ ] Component Diagram (Sơ đồ thành phần)
- [ ] Deployment Diagram (Sơ đồ triển khai)

### Tài liệu kỹ thuật:
- [ ] Software Requirements Specification (SRS)
- [ ] Software Design Document (SDD)
- [ ] Test Plan
- [ ] User Manual
- [ ] API Documentation

---

## 🔧 Chỉnh sửa sơ đồ

Nếu muốn sửa sơ đồ, chỉnh file `.puml`:

### Thêm Use Case mới:
```plantuml
usecase (Tên use case mới) as UC99
Actor --> UC99
```

### Thêm relationship:
```plantuml
UC1 ..> UC2 : <<include>>
UC3 ..> UC4 : <<extend>>
```

### Thêm note:
```plantuml
note right of Actor
  Ghi chú ở đây
end note
```

### Styling:
```plantuml
skinparam actorStyle awesome
skinparam packageBackgroundColor LightYellow
skinparam usecaseBorderColor DarkBlue
```

---

## 📞 Liên hệ

Nếu cần hỗ trợ về tài liệu thiết kế, liên hệ:
- Email: admin@freshberry.vn
- Project: FreshBerry Fruit Shop

---

**Lưu ý:** Sơ đồ được vẽ dựa trên phân tích chức năng thực tế của hệ thống. Có thể bổ sung thêm use case khi phát triển tính năng mới.

**Version:** 1.0  
**Last updated:** 2025-10-26

