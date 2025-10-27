# 📊 SƠ ĐỒ USE CASE - FRESHBERRY FRUIT SHOP

## 🎯 Tài liệu đã được tạo hoàn chỉnh!

Tất cả tài liệu thiết kế Use Case Diagram đã được tạo trong thư mục **`docs/`**

---

## 📁 CẤU TRÚC THƯ MỤC

```
fruitshop/
├── docs/                                    ⭐ THƯ MỤC TÀI LIỆU
│   ├── INDEX.md                            📚 Điểm bắt đầu - Mục lục tổng quát
│   ├── QUICK-START.md                      🚀 Xem sơ đồ trong 2 phút
│   ├── USE-CASE-SUMMARY.md                 📊 Tóm tắt 46+ use cases
│   ├── README.md                           📖 Hướng dẫn chi tiết tools
│   ├── LAYOUT-GUIDE.md                     📐 Hướng dẫn Layout Vertical ⭐NEW
│   ├── use-case-description.md             📝 Mô tả đầy đủ từng use case
│   ├── use-case-diagram.puml               🎨 Sơ đồ đầy đủ (VERTICAL) ⬇️
│   ├── use-case-diagram-simple.puml        🎨 Sơ đồ đơn giản (VERTICAL) ⬇️
│   └── view-diagram.html                   🌐 Web viewer (mở browser)
│
├── accounts/                               # UC1-UC6: Tài khoản
├── products/                               # UC10-UC20: Sản phẩm
├── orders/                                 # UC30-UC57: Đơn hàng
├── delivery/                               # UC70-UC79: Giao hàng
├── reports/                                # UC90-UC97: Báo cáo
└── fruitshop/                              # Settings Django
```

---

## 🚀 CÁCH XEM SƠ ĐỒ (2 PHÚT)

### Bước 1: Mở file sơ đồ
```bash
cd docs
notepad use-case-diagram.puml
# Hoặc mở bằng VS Code, Notepad++
```

### Bước 2: Copy toàn bộ nội dung
- Nhấn **Ctrl+A** (Select All)
- Nhấn **Ctrl+C** (Copy)

### Bước 3: Xem online
1. Truy cập: **http://www.plantuml.com/plantuml/uml/**
2. Paste nội dung vào (Ctrl+V)
3. Click "Submit"
4. ✅ Sơ đồ hiển thị!

### Bước 4: Download (Tùy chọn)
- Click **PNG** để tải ảnh
- Click **SVG** để tải vector (chất lượng tốt nhất)
- Click **PDF** để in

---

## 📚 CÁC FILE QUAN TRỌNG

### 🎨 Sơ đồ Use Case (PlantUML)

#### 1. `use-case-diagram.puml` - Đầy đủ chi tiết
- **Layout:** **VERTICAL (Dọc)** ⬇️ Top to Bottom ⭐
- **46+ Use Cases** được vẽ đầy đủ
- **4 Actors:** Khách hàng, Admin, Shipper, Hệ thống (VNPay, Email)
- **7 Packages:** Nhóm chức năng logic
- **Relationships:** Include, Extend, Association
- **Notes:** Giải thích chi tiết
- **Size:** ~800x2000 pixels (Portrait)
- **✅ Tốt cho:** In A4, Presentation, Workflow

#### 2. `use-case-diagram-simple.puml` - Đơn giản hóa
- **Layout:** **VERTICAL (Dọc)** ⬇️ Top to Bottom ⭐
- Nhóm use cases thành chức năng chính
- Dễ nhìn, dễ hiểu hơn
- **Size:** ~600x1200 pixels (Portrait)
- **✅ Tốt cho:** Overview nhanh, In 1 trang A4

### 📝 Tài liệu mô tả

#### 1. `use-case-description.md` - Chi tiết đầy đủ (⭐⭐⭐)
**46+ Use Cases** được mô tả với:
- Actor thực hiện
- Mô tả chức năng
- Luồng chính (Main flow)
- Luồng ngoại lệ (Alternative flow)
- Quan hệ Include/Extend

**Ví dụ:**
```markdown
### UC34: Thanh toán (Checkout)
- Actor: Khách hàng
- Mô tả: Hoàn tất đơn hàng
- Luồng chính:
  1. Nhập địa chỉ giao hàng
  2. Áp dụng mã giảm giá (UC35)
  3. Chọn phương thức thanh toán (UC36)
  4. Xác nhận đơn hàng (UC39)
  5. Gửi email xác nhận (UC100)
```

#### 2. `USE-CASE-SUMMARY.md` - Tóm tắt nhanh (⭐⭐)
- Tóm tắt 46+ use cases
- Phân bổ theo actor (Customer: 24, Admin: 20, Shipper: 6)
- **Top 10 use cases** quan trọng nhất
- **3 Workflows** nghiệp vụ chính
- Checklist đánh giá

#### 3. `QUICK-START.md` - Bắt đầu nhanh (⭐)
- Xem sơ đồ trong 2 phút
- Lộ trình đọc tài liệu (3 levels)
- Tips và FAQ

#### 4. `README.md` - Hướng dẫn tools
- 5 cách xem sơ đồ PlantUML
- Cài đặt VS Code + PlantUML extension
- Export PNG/SVG/PDF

#### 5. `INDEX.md` - Mục lục tổng quát
- Điểm bắt đầu cho mọi người
- Hướng dẫn theo vai trò (Sinh viên, Giảng viên, Developer)

### 🌐 Web Viewer

#### `view-diagram.html` - Mở bằng browser
**4 Tabs:**
1. **Tổng quan** - Thống kê, cards đẹp
2. **Sơ đồ Use Case** - Links xem online
3. **Hướng dẫn xem** - 5 cách xem PlantUML
4. **Chi tiết Use Cases** - Top 10, mô tả

**Giao diện:**
- Responsive design
- Modern UI với gradient
- Tab navigation
- Cards thống kê màu sắc

---

## 📊 THỐNG KÊ USE CASE

### 46+ Use Cases phân bổ theo Package:

| Package | Use Cases | Apps Django |
|---------|-----------|-------------|
| 1. Quản lý Tài khoản | 6 | accounts |
| 2. Quản lý Sản phẩm | 11 | products |
| 3. Giỏ hàng & Đặt hàng | 10 | orders |
| 4. Quản lý Đơn hàng | 8 | orders |
| 5. Quản lý Giao hàng | 10 | delivery |
| 6. Báo cáo & Thống kê | 8 | reports |
| 7. Hệ thống Thông báo | 4 | email system |
| **TỔNG** | **46+** | **5 apps** |

### Phân bổ theo Actor:

| Actor | Use Cases | Mô tả |
|-------|-----------|-------|
| 👤 **Khách hàng** | 24 | Mua sắm, đặt hàng, tracking |
| 👨‍💼 **Admin** | 20 | Quản lý toàn bộ hệ thống |
| 🚚 **Shipper** | 6 | Giao hàng, cập nhật |
| 🔧 **Hệ thống** | 6 | VNPay (2), Email (4) |

---

## ⭐ TOP 10 USE CASES QUAN TRỌNG NHẤT

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

## 🔄 3 QUY TRÌNH NGHIỆP VỤ CHÍNH

### 1️⃣ Customer Journey (Khách hàng mua hàng)
```
Browse Products → View Details → Add to Cart → Login 
→ Checkout → Apply Discount → Choose Payment (VNPay/COD) 
→ Confirm Order → Receive Email → Track Order → Review
```

### 2️⃣ Admin Workflow (Xử lý đơn hàng)
```
Receive Order (Pending) → Confirm → Processing 
→ Assign Shipper → Send Email → Update Status 
→ Shipped → Delivered → Completed
```

### 3️⃣ Shipper Workflow (Giao hàng)
```
Receive Email → View Orders → Pick Up → In Transit 
→ Update Real-time → Delivered (Upload Photo) 
OR Failed (Report Reason)
```

---

## 🎯 LỘ TRÌNH ĐỌC TÀI LIỆU

### Level 1: Hiểu tổng quan (10 phút) ⭐
1. Đọc `docs/QUICK-START.md`
2. Xem sơ đồ đơn giản: `use-case-diagram-simple.puml`
3. Đọc `docs/USE-CASE-SUMMARY.md`

### Level 2: Hiểu chi tiết (30 phút) ⭐⭐
1. Xem sơ đồ đầy đủ: `use-case-diagram.puml`
2. Đọc Top 10 UCs trong `use-case-description.md`
3. Mở `view-diagram.html` trong browser

### Level 3: Master (2 giờ) ⭐⭐⭐
1. Đọc toàn bộ `use-case-description.md` (46+ UCs)
2. Phân tích 3 workflows nghiệp vụ
3. Map với code Django
4. Vẽ sequence diagrams cho use cases quan trọng

---

## 🛠️ CÔNG CỤ VÀ LINKS

### Xem sơ đồ online (Không cần cài đặt):
- 🌐 **PlantUML Official:** http://www.plantuml.com/plantuml/uml/
- 🌐 **PlantUML Editor:** https://plantuml-editor.kkeisuke.com/
- 🌐 **PlantText:** https://www.planttext.com/

### Download tools:
- 📥 **Java (Required):** https://www.java.com/download/
- 📥 **VS Code:** https://code.visualstudio.com/
- 📥 **PlantUML Extension:** Search "PlantUML" by jebbs in VS Code

### Tài liệu tham khảo:
- 📖 [PlantUML Use Case Syntax](https://plantuml.com/use-case-diagram)
- 📖 [UML Best Practices](https://www.uml-diagrams.org/use-case-diagrams.html)

---

## ✅ CHECKLIST SỬ DỤNG

### Cho báo cáo / đồ án:
- [ ] Đã xem sơ đồ đầy đủ
- [ ] Đã export PNG/SVG/PDF
- [ ] Đã đọc mô tả chi tiết 46+ UCs
- [ ] Đã hiểu relationships (Include/Extend)
- [ ] Đã phân tích 3 workflows

### Cho presentation:
- [ ] Export sơ đồ độ phân giải cao
- [ ] Print Top 10 use cases
- [ ] Chuẩn bị demo workflows
- [ ] Giải thích actors và packages

### Cho implementation:
- [ ] Đọc toàn bộ use-case-description.md
- [ ] Map use cases với Django views
- [ ] Implement theo workflows
- [ ] Test coverage cho từng use case

---

## 💡 TIPS HAY

### Nếu sơ đồ quá lớn:
✅ Xem file `use-case-diagram-simple.puml` trước

### Nếu muốn in:
✅ Export dạng **PDF** hoặc **SVG** (độ phân giải cao)

### Nếu muốn chỉnh sửa:
✅ Cài **VS Code + PlantUML extension**, edit file `.puml`

### Nếu embed vào Word/PowerPoint:
✅ Export PNG độ phân giải cao, insert as image

---

## ❓ FAQ

**Q: Tại sao không thấy ảnh sơ đồ?**  
A: File `.puml` là source code. Cần render bằng PlantUML hoặc xem online.

**Q: Có cần cài PlantUML không?**  
A: Không bắt buộc. Dùng online viewer là nhanh nhất.

**Q: File .puml mở bằng gì?**  
A: Notepad, VS Code, hoặc text editor bất kỳ.

**Q: Làm sao export ra ảnh?**  
A: Xem online rồi click "PNG" hoặc "SVG" để download.

**Q: Có thể chỉnh sửa sơ đồ không?**  
A: Có! Edit file `.puml`, sau đó render lại.

---

## 🎓 KẾT LUẬN

✅ **Hoàn thành:** Tài liệu Use Case Diagram đầy đủ  
✅ **46+ Use Cases** được mô tả chi tiết  
✅ **Sơ đồ chuẩn UML** (PlantUML)  
✅ **7 Files tài liệu** trong thư mục `docs/`  
✅ **Multiple formats:** PUML, MD, HTML  
✅ **3 Workflows** nghiệp vụ được phân tích  

**Điểm mạnh:**
- Tài liệu đầy đủ, chuyên nghiệp
- Nhiều cách xem sơ đồ
- Có cả phiên bản đơn giản và chi tiết
- Web viewer tiện lợi
- Checklist đánh giá rõ ràng

**Sử dụng cho:**
- 📄 Báo cáo đồ án / Luận văn
- 🎯 Tài liệu thiết kế hệ thống
- 👨‍💻 Hướng dẫn phát triển
- 🎤 Presentation / Demo

---

## 🚀 BẮT ĐẦU NGAY

### Xem sơ đồ ngay (2 phút):
```bash
cd docs
# Mở QUICK-START.md và làm theo hướng dẫn
```

### Đọc tài liệu đầy đủ:
```bash
cd docs
# Mở INDEX.md để bắt đầu
```

### Xem web viewer:
```bash
cd docs
# Mở view-diagram.html bằng browser
```

---

## 📞 THÔNG TIN

**Project:** FreshBerry Fruit Shop  
**Technology:** Django 5.2+, MySQL, VNPay, Gmail SMTP  
**Documentation Version:** 1.0  
**Created:** 2025-10-26  

**Structure:**
```
5 Django Apps:
├── accounts   → UC1-UC6   (Tài khoản)
├── products   → UC10-UC20 (Sản phẩm)
├── orders     → UC30-UC57 (Đơn hàng)
├── delivery   → UC70-UC79 (Giao hàng)
└── reports    → UC90-UC97 (Báo cáo)
```

---

## 🎉 DONE!

Tất cả tài liệu Use Case Diagram đã được tạo xong!

**➡️ Bắt đầu từ:** `docs/INDEX.md` hoặc `docs/QUICK-START.md`

**Happy Learning! 📚✨**

