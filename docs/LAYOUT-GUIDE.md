# 📐 HƯỚNG DẪN LAYOUT SƠ ĐỒ USE CASE

## 🎯 Layout đã được thay đổi thành VERTICAL (Dọc)

Tất cả các file sơ đồ Use Case đã được cập nhật để hiển thị theo **chiều dọc (top to bottom)** thay vì ngang!

---

## 📊 CÁC FILE SƠ ĐỒ

### ✅ Tất cả đã là VERTICAL LAYOUT:

| File | Layout | Mô tả |
|------|--------|-------|
| `use-case-diagram.puml` | **Dọc** ⬇️ | Sơ đồ đầy đủ 46+ UCs |
| `use-case-diagram-simple.puml` | **Dọc** ⬇️ | Sơ đồ đơn giản |

---

## 🔧 THAY ĐỔI KỸ THUẬT

### Code đã thêm vào mỗi file:

```plantuml
' Layout - Top to Bottom (Vertical)
top to bottom direction
```

**Giải thích:**
- `top to bottom direction` - Sắp xếp các phần tử từ **trên xuống dưới**
- Mặc định PlantUML sử dụng layout tự động (thường ngang)
- Directive này buộc layout dọc

---

## 📸 KẾT QUẢ

### Trước (Horizontal):
```
[Customer] ---> (UC1)  (UC2)  (UC3)  (UC4) ---> [Admin]
                 |      |      |      |
              (UC5)  (UC6)  (UC7)  (UC8)
```

### Sau (Vertical): ⭐
```
      [Customer]
          |
       (UC1)
          |
       (UC2)
          |
       (UC3)
          |
       (UC4)
          ↓
       [Admin]
```

---

## 🚀 CÁCH XEM SƠ ĐỒ VERTICAL

### Online (Nhanh nhất):

1. Mở file: `use-case-diagram.puml` hoặc `use-case-diagram-simple.puml`
2. Copy toàn bộ (Ctrl+A, Ctrl+C)
3. Truy cập: http://www.plantuml.com/plantuml/uml/
4. Paste vào (Ctrl+V)
5. ✅ **Sơ đồ hiển thị DỌC!**

### VS Code:

1. Cài extension **PlantUML** by jebbs
2. Mở file `.puml`
3. Nhấn **Alt + D** để preview
4. ✅ Sơ đồ hiển thị dọc

---

## 🎨 ƯU ĐIỂM LAYOUT DỌC

✅ **Dễ đọc hơn** - Theo thói quen đọc từ trên xuống  
✅ **In ấn tốt** - Phù hợp với khổ giấy A4 dọc  
✅ **Presentation** - Tốt cho slide PowerPoint  
✅ **Luồng logic** - Workflow từ trên xuống dễ hiểu  
✅ **Ít scroll ngang** - Xem trên màn hình dọc thuận tiện  

---

## 📏 SO SÁNH LAYOUT

### Horizontal Layout (Ngang):
- ✅ Tốt cho màn hình rộng (widescreen)
- ✅ Nhiều thông tin trên 1 hàng
- ❌ Khó in (cần giấy A3 ngang)
- ❌ Phải scroll ngang nhiều

### Vertical Layout (Dọc): ⭐
- ✅ **Dễ in trên A4**
- ✅ **Dễ đọc trên mobile/tablet**
- ✅ **Luồng workflow rõ ràng**
- ✅ **Ít scroll ngang**
- ❌ Có thể dài hơn (scroll dọc nhiều)

---

## 🔄 MUỐN ĐỔI LẠI LAYOUT NGANG?

Nếu bạn muốn layout ngang (horizontal), chỉ cần:

### Cách 1: Bỏ directive
Xóa dòng này trong file `.puml`:
```plantuml
top to bottom direction
```

### Cách 2: Đổi sang left to right
Thay bằng:
```plantuml
left to right direction
```

### Cách 3: Để PlantUML tự động
Comment out directive:
```plantuml
' top to bottom direction
```

---

## 📦 FILE BACKUP (Nếu cần)

Nếu bạn muốn giữ cả 2 versions:

### Tạo file mới cho layout ngang:
```bash
cd docs
copy use-case-diagram.puml use-case-diagram-horizontal.puml
```

Sau đó chỉnh sửa file mới:
- Xóa `top to bottom direction`
- Thêm `left to right direction`
- Đổi title thành "Horizontal Layout"

---

## ✅ CHECKLIST CẬP NHẬT

- [x] `use-case-diagram.puml` - Đã đổi sang vertical
- [x] `use-case-diagram-simple.puml` - Đã đổi sang vertical
- [x] Title đã update: "Vertical Layout"
- [x] Directive `top to bottom direction` đã thêm

---

## 💡 TIPS XEM SƠ ĐỒ VERTICAL

### 1. Zoom to fit:
Khi xem online, click nút **"Zoom to fit"** để xem toàn bộ sơ đồ

### 2. Export PDF:
```
1. Xem online
2. Click "PDF" 
3. ✅ File PDF sẵn sàng in
```

### 3. Export PNG (High Resolution):
```
1. Xem online
2. Click "PNG"
3. Download
4. ✅ Ảnh chất lượng cao
```

### 4. Export SVG (Vector):
```
1. Xem online
2. Click "SVG"
3. ✅ Vector - scale lên không bị vỡ
```

---

## 📊 KẾT QUẢ MONG ĐỢI

### Với file `use-case-diagram.puml`:
- **Height:** ~2000-2500 pixels
- **Width:** ~800-1000 pixels
- **Aspect Ratio:** Portrait (dọc)
- **A4 Pages:** 2-3 trang dọc

### Với file `use-case-diagram-simple.puml`:
- **Height:** ~1200-1500 pixels
- **Width:** ~600-800 pixels
- **Aspect Ratio:** Portrait (dọc)
- **A4 Pages:** 1-2 trang dọc

---

## 🎓 KẾT LUẬN

✅ **Layout đã chuyển sang VERTICAL**  
✅ **Tốt hơn cho in ấn và presentation**  
✅ **Dễ đọc hơn trên màn hình thông thường**  
✅ **Workflow từ trên xuống dễ hiểu**  

**Bây giờ bạn có thể:**
- ✅ Xem sơ đồ vertical online
- ✅ In trên giấy A4 dọc
- ✅ Sử dụng cho slide PowerPoint
- ✅ Dễ dàng theo dõi workflow

---

## 🚀 BẮT ĐẦU NGAY

### Xem sơ đồ vertical:
1. Mở `use-case-diagram.puml`
2. Copy toàn bộ
3. Paste vào: http://www.plantuml.com/plantuml/uml/
4. ✅ **Xem sơ đồ DỌC!**

---

**Happy Diagramming! 📊⬇️**

*Cập nhật: 2025-10-27 - Layout vertical*


