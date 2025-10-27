# 📚 TÀI LIỆU THIẾT KẾ - FRESHBERRY FRUIT SHOP

## 🎯 MỤC LỤC TỔNG QUÁT

> **Tài liệu Use Case Diagram hoàn chỉnh cho hệ thống FreshBerry Fruit Shop**

---

## 📁 CẤU TRÚC THƯ MỤC `docs/`

```
docs/
├── INDEX.md                          ⭐ File này - Điểm bắt đầu
├── QUICK-START.md                    🚀 Xem sơ đồ trong 2 phút
├── USE-CASE-SUMMARY.md               📊 Tóm tắt 46+ use cases
├── README.md                         📖 Hướng dẫn chi tiết
├── LAYOUT-GUIDE.md                   📐 Hướng dẫn Layout Vertical
├── use-case-description.md           📝 Mô tả đầy đủ từng use case
├── use-case-diagram.puml             🎨 Sơ đồ đầy đủ (VERTICAL) ⬇️
├── use-case-diagram-simple.puml      🎨 Sơ đồ đơn giản (VERTICAL) ⬇️
└── view-diagram.html                 🌐 Web viewer (mở browser)
```

---

## 🎯 BẮT ĐẦU TỪ ĐÂU?

### 👨‍🎓 Sinh viên / Người mới
**Mục tiêu:** Hiểu tổng quan hệ thống

1. ✅ **[QUICK-START.md](QUICK-START.md)** - Xem sơ đồ ngay (2 phút)
2. ✅ **[USE-CASE-SUMMARY.md](USE-CASE-SUMMARY.md)** - Tóm tắt 46+ UCs (10 phút)
3. ✅ **[use-case-diagram-simple.puml](use-case-diagram-simple.puml)** - Sơ đồ đơn giản
4. ✅ **[use-case-description.md](use-case-description.md)** - Đọc Top 10 UCs

### 👨‍🏫 Giảng viên / Người đánh giá
**Mục tiêu:** Kiểm tra tính đầy đủ và chính xác

1. ✅ **[view-diagram.html](view-diagram.html)** - Mở browser xem overview
2. ✅ **[use-case-diagram.puml](use-case-diagram.puml)** - Sơ đồ đầy đủ chi tiết
3. ✅ **[use-case-description.md](use-case-description.md)** - Mô tả 46+ UCs
4. ✅ **[USE-CASE-SUMMARY.md](USE-CASE-SUMMARY.md)** - Checklist đánh giá

### 👨‍💻 Developers
**Mục tiêu:** Implement theo thiết kế

1. ✅ **[README.md](README.md)** - Cài đặt tools (VS Code + PlantUML)
2. ✅ **[use-case-diagram.puml](use-case-diagram.puml)** - Source code sơ đồ
3. ✅ **[use-case-description.md](use-case-description.md)** - Đọc toàn bộ
4. ✅ Xem code trong `../accounts/`, `../products/`, `../orders/`, `../delivery/`, `../reports/`

---

## 📊 THỐNG KÊ DỰ ÁN

| Chỉ số | Giá trị |
|--------|---------|
| **Use Cases** | 46+ |
| **Actors** | 4 (Khách hàng, Admin, Shipper, Hệ thống) |
| **Packages** | 7 modules chức năng |
| **Django Apps** | 5 (accounts, products, orders, delivery, reports) |
| **Models** | 20+ |
| **Views** | 50+ |
| **Templates** | 40+ |

---

## 🎨 CÁC FILE SƠ ĐỒ

### 1. **use-case-diagram.puml** (Đầy đủ) ⭐
- **Mô tả:** Sơ đồ Use Case hoàn chỉnh với 46+ use cases
- **Layout:** **VERTICAL (Dọc)** ⬇️ - Top to Bottom
- **Nội dung:**
  - 4 Actors với icon đẹp
  - 7 Packages được nhóm rõ ràng
  - Include/Extend relationships
  - Notes giải thích
- **Kích thước:** ~800x2000 pixels (Portrait)
- **Dùng khi:** Báo cáo chính thức, presentation, in A4

### 2. **use-case-diagram-simple.puml** (Đơn giản) 
- **Mô tả:** Sơ đồ đơn giản hóa, dễ nhìn hơn
- **Layout:** **VERTICAL (Dọc)** ⬇️ - Top to Bottom
- **Nội dung:**
  - Nhóm use cases thành các chức năng chính
  - Giảm chi tiết, giữ cấu trúc tổng quan
- **Kích thước:** ~600x1200 pixels (Portrait)
- **Dùng khi:** Muốn overview nhanh, in 1 trang A4

### Cách xem sơ đồ:
```bash
# Option 1: Online (Nhanh nhất)
1. Copy nội dung file .puml
2. Paste vào: http://www.plantuml.com/plantuml/uml/

# Option 2: VS Code (Developers)
1. Cài extension "PlantUML" by jebbs
2. Mở file .puml
3. Alt + D để preview

# Option 3: Export ảnh
puml generate use-case-diagram.puml -o .
```

---

## 📝 TÀI LIỆU MÔ TẢ

### 1. **use-case-description.md** (Chi tiết) ⭐⭐⭐
**Nội dung:**
- Mô tả đầy đủ 46+ use cases
- Luồng chính (Main flow)
- Luồng ngoại lệ (Alternative flow)
- Điều kiện, kết quả mong đợi
- Quan hệ giữa các use case

**Cấu trúc:**
```
Package 1: Quản lý Tài khoản (6 UCs)
  UC1: Đăng ký tài khoản
  UC2: Đăng nhập
  ...

Package 2: Quản lý Sản phẩm (11 UCs)
  UC10: Xem danh sách sản phẩm
  UC11: Tìm kiếm sản phẩm
  ...

... (7 packages)
```

### 2. **USE-CASE-SUMMARY.md** (Tóm tắt) ⭐⭐
**Nội dung:**
- Tóm tắt nhanh 46+ use cases
- Phân bổ use case theo actor
- Top 10 use cases quan trọng
- Quy trình nghiệp vụ (3 workflows)
- Checklist đánh giá

### 3. **README.md** (Hướng dẫn) ⭐
**Nội dung:**
- Hướng dẫn cài đặt tools
- 5 cách xem sơ đồ PlantUML
- Chỉnh sửa và export
- FAQ

### 4. **QUICK-START.md** (Bắt đầu nhanh) ⭐
**Nội dung:**
- Xem sơ đồ trong 2 phút
- Lộ trình đọc tài liệu (3 levels)
- Tips và FAQ
- Checklist

---

## 🌐 WEB VIEWER

### **view-diagram.html**
Mở file này bằng browser để xem:
- Tab 1: **Tổng quan** - Thống kê, actors, packages
- Tab 2: **Sơ đồ Use Case** - Links xem sơ đồ online
- Tab 3: **Hướng dẫn xem** - 5 cách xem PlantUML
- Tab 4: **Chi tiết Use Cases** - Top 10, mô tả ngắn

**Giao diện:**
- Responsive design
- Tab navigation đẹp
- Cards thống kê màu sắc
- Links trực tiếp đến tools

---

## 🔗 LINKS NHANH

### Xem sơ đồ online:
- 🌐 [PlantUML Official](http://www.plantuml.com/plantuml/uml/)
- 🌐 [PlantUML Editor](https://plantuml-editor.kkeisuke.com/)
- 🌐 [PlantText](https://www.planttext.com/)

### Download tools:
- 📥 [Java JDK](https://www.java.com/download/)
- 📥 [VS Code](https://code.visualstudio.com/)
- 📥 [PlantUML JAR](https://plantuml.com/download)

### Tài liệu tham khảo:
- 📖 [PlantUML Syntax](https://plantuml.com/use-case-diagram)
- 📖 [UML Use Case Best Practices](https://www.uml-diagrams.org/use-case-diagrams.html)

---

## 📚 NỘI DUNG CHI TIẾT

### 🎭 4 Actors

| Actor | Use Cases | Vai trò |
|-------|-----------|---------|
| **Khách hàng** | 24 | Mua sắm, đặt hàng, theo dõi |
| **Admin** | 20 | Quản lý toàn bộ hệ thống |
| **Shipper** | 6 | Giao hàng, cập nhật |
| **Hệ thống** | 6 | VNPay (2), Email (4) |

### 📦 7 Packages

1. **Quản lý Tài khoản** (6 UCs) - Accounts module
2. **Quản lý Sản phẩm** (11 UCs) - Products module
3. **Giỏ hàng & Đặt hàng** (10 UCs) - Orders module (Cart)
4. **Quản lý Đơn hàng** (8 UCs) - Orders module (Management)
5. **Quản lý Giao hàng** (10 UCs) - Delivery module
6. **Báo cáo & Thống kê** (8 UCs) - Reports module
7. **Hệ thống Thông báo** (4 UCs) - Email system

### ⭐ Top 10 Use Cases quan trọng

1. **UC34** - Thanh toán (⭐⭐⭐⭐⭐)
2. **UC12** - Xem chi tiết sản phẩm (⭐⭐⭐⭐⭐)
3. **UC54** - Quản lý đơn hàng - Admin (⭐⭐⭐⭐⭐)
4. **UC70** - Phân công shipper (⭐⭐⭐⭐)
5. **UC73** - Cập nhật giao hàng (⭐⭐⭐⭐)
6. **UC90** - Dashboard (⭐⭐⭐⭐)
7. **UC37** - Thanh toán VNPay (⭐⭐⭐⭐)
8. **UC18** - Quản lý sản phẩm (⭐⭐⭐)
9. **UC15** - Đánh giá sản phẩm (⭐⭐⭐)
10. **UC91** - Báo cáo doanh thu (⭐⭐⭐)

---

## 🔄 3 QUY TRÌNH NGHIỆP VỤ CHÍNH

### 1. Customer Journey (Mua hàng)
```
Duyệt → Chi tiết → Thêm giỏ → Login → Checkout → Thanh toán → Tracking → Đánh giá
```

### 2. Admin Workflow (Xử lý đơn)
```
Nhận đơn → Xác nhận → Chuẩn bị → Phân công shipper → Cập nhật trạng thái
```

### 3. Shipper Workflow (Giao hàng)
```
Nhận email → Xem đơn → Lấy hàng → Đang giao → Giao thành công/thất bại
```

---

## ✅ CHECKLIST SỬ DỤNG TÀI LIỆU

### Cho báo cáo (Report):
- [ ] Đã xem sơ đồ đầy đủ
- [ ] Đã export PNG/PDF
- [ ] Đã đọc mô tả chi tiết
- [ ] Đã hiểu relationships
- [ ] Đã phân tích 3 workflows

### Cho presentation (Thuyết trình):
- [ ] Export sơ đồ độ phân giải cao
- [ ] In TOP 10 use cases
- [ ] Chuẩn bị demo workflows
- [ ] Giải thích actors và packages

### Cho implementation (Phát triển):
- [ ] Đọc toàn bộ use-case-description.md
- [ ] Map use cases với Django views
- [ ] Implement theo workflows
- [ ] Test từng use case

---

## 🎓 KẾT LUẬN

Thư mục `docs/` chứa tài liệu Use Case Diagram hoàn chỉnh cho hệ thống **FreshBerry Fruit Shop** với:

✅ **Sơ đồ chuẩn UML** (PlantUML)  
✅ **46+ Use Cases** được mô tả chi tiết  
✅ **4 Actors** được định nghĩa rõ ràng  
✅ **7 Packages** nhóm chức năng logic  
✅ **Relationships** (Include/Extend) chính xác  
✅ **3 Workflows** nghiệp vụ chính  
✅ **Multiple formats** (PUML, MD, HTML)  

**Điểm mạnh:**
- Tài liệu đầy đủ, dễ hiểu
- Nhiều cách xem sơ đồ
- Có cả phiên bản đơn giản và chi tiết
- Web viewer tiện lợi
- Checklist đánh giá

**Sử dụng cho:**
- Báo cáo đồ án / Luận văn
- Tài liệu thiết kế hệ thống
- Hướng dẫn phát triển
- Presentation / Demo

---

## 📞 THÔNG TIN THÊM

**Project:** FreshBerry Fruit Shop  
**Tech:** Django 5.2+, MySQL, VNPay, Gmail SMTP  
**Version:** 1.0  
**Date:** 2025-10-26  

**Repository structure:**
```
fruitshop/
├── accounts/          # UC1-UC6
├── products/          # UC10-UC20
├── orders/            # UC30-UC57
├── delivery/          # UC70-UC79
├── reports/           # UC90-UC97
├── docs/             # ← Thư mục này
└── ...
```

---

## 🚀 BẮT ĐẦU NGAY

**Nếu bạn chỉ có 5 phút:**
1. Đọc [QUICK-START.md](QUICK-START.md)
2. Xem sơ đồ online: http://www.plantuml.com/plantuml/uml/
3. Đọc [USE-CASE-SUMMARY.md](USE-CASE-SUMMARY.md)

**Nếu bạn có 30 phút:**
1. Mở [view-diagram.html](view-diagram.html) trong browser
2. Xem sơ đồ đầy đủ: [use-case-diagram.puml](use-case-diagram.puml)
3. Đọc Top 10 UCs trong [use-case-description.md](use-case-description.md)

**Nếu bạn muốn master (2 giờ):**
1. Đọc toàn bộ [use-case-description.md](use-case-description.md)
2. Phân tích 3 workflows
3. Map với code Django
4. Vẽ sequence diagrams

---

**Happy Learning! 🎉**

*Tài liệu này được tạo tự động dựa trên phân tích hệ thống thực tế.*

