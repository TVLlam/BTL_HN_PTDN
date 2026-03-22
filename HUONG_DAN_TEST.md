# 📋 HƯỚNG DẪN CHẠY VÀ TEST DỰ ÁN TỪ ĐẦU ĐẾN CUỐI

> **Dự án**: ERP Quản lý Nhân sự – Khách hàng – Văn bản  
> **Nền tảng**: Odoo 15.0 · Python 3.10 · PostgreSQL 10  
> **Hệ điều hành**: Ubuntu / WSL2

---

## Mục lục

1. [Yêu cầu hệ thống](#1-yêu-cầu-hệ-thống)
2. [Cài đặt môi trường](#2-cài-đặt-môi-trường)
3. [Cấu hình dự án](#3-cấu-hình-dự-án)
4. [Khởi chạy dự án lần đầu](#4-khởi-chạy-dự-án-lần-đầu)
5. [Cài đặt module](#5-cài-đặt-module)
6. [Test Module Nhân sự (HRM)](#6-test-module-nhân-sự-hrm)
7. [Test Module CRM (Khách hàng & Bán hàng)](#7-test-module-crm-khách-hàng--bán-hàng)
8. [Test Module QLVB (Quản lý Văn bản)](#8-test-module-qlvb-quản-lý-văn-bản)
9. [Test Email thông báo](#9-test-email-thông-báo)
10. [Test Báo cáo nâng cao](#10-test-báo-cáo-nâng-cao)
11. [Test Chatbot AI](#11-test-chatbot-ai)
12. [Lệnh cập nhật module](#12-lệnh-cập-nhật-module)
13. [Xử lý lỗi thường gặp](#13-xử-lý-lỗi-thường-gặp)

---

## 1. Yêu cầu hệ thống

| Phần mềm | Phiên bản tối thiểu | Ghi chú |
|-----------|---------------------|---------|
| Python | 3.10+ | Khuyến nghị 3.10.x |
| Docker | 20.10+ | Để chạy PostgreSQL |
| Docker Compose | 1.29+ | Hoặc docker compose (v2) |
| Git | 2.x | Clone dự án |
| pip | 21+ | Cài thư viện Python |
| Trình duyệt | Chrome/Firefox mới nhất | Truy cập giao diện web |

---

## 2. Cài đặt môi trường

### Bước 2.1: Clone dự án

```bash
git clone <url-repository> TTDN-16-01-N4
cd TTDN-16-01-N4
```

### Bước 2.2: Khởi động PostgreSQL bằng Docker

```bash
# Khởi động PostgreSQL container
docker-compose up -d

# Kiểm tra container đang chạy
docker ps
# → Phải thấy: postgres_odoo-base-15-01 ở trạng thái Up, port 5431
```

> **Lưu ý**: PostgreSQL chạy trên port **5431** (không phải 5432 mặc định)

### Bước 2.3: Cài đặt thư viện Python

```bash
# Cài đặt requirements
pip install -r requirements.txt

# Cài thêm các thư viện bắt buộc cho module custom
pip install cryptography==41.0.7 pyOpenSSL==23.3.0 urllib3==1.26.18
```

> **Quan trọng**: Phải dùng đúng phiên bản `cryptography==41.0.7` và `pyOpenSSL==23.3.0` để tránh lỗi `Cannot import name 'x509' from 'cryptography'`

### Bước 2.4: Kiểm tra kết nối PostgreSQL

```bash
# Test kết nối (password: odoo)
psql -h localhost -p 5431 -U odoo -d postgres -c "SELECT 1;"
```

---

## 3. Cấu hình dự án

### Bước 3.1: File odoo.conf

File `odoo.conf` đã có sẵn cấu hình:

```ini
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```

### Bước 3.2: File .env (BẮT BUỘC)

Mở file `.env` ở thư mục gốc dự án và cập nhật:

```env
# API Key cho Chatbot AI (Gemini)
GEMINI_API_KEY=your-gemini-api-key-here

# Gmail thong bao - Thay bang email va App Password cua ban
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

#### Cách lấy Gmail App Password:

1. Truy cập https://myaccount.google.com/security
2. Bật **Xác minh 2 bước** (2-Step Verification) nếu chưa bật
3. Vào **Mật khẩu ứng dụng** (App Passwords)
4. Tạo mật khẩu mới → Chọn app: "Thư" → Chọn thiết bị: "Khác" → Đặt tên "Odoo ERP"
5. Copy mã 16 ký tự (dạng `xxxx xxxx xxxx xxxx`) vào `GMAIL_APP_PASSWORD`

#### Cách lấy Gemini API Key:

1. Truy cập https://aistudio.google.com/apikey
2. Nhấn **Create API Key**
3. Copy key vào `GEMINI_API_KEY`

---

## 4. Khởi chạy dự án lần đầu

### Bước 4.1: Tạo database và cài module cơ bản

```bash
# Chạy lần đầu - tự tạo database "tranvanlam" và cài module base
python3 odoo-bin.py -c odoo.conf -d tranvanlam --stop-after-init
```

### Bước 4.2: Cài 3 module chính

```bash
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -i nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init
```

> **Lưu ý**: Lệnh `-i` (install) dùng cho lần cài đầu tiên. Nếu module đã cài rồi, dùng `-u` (update).

### Bước 4.3: Khởi chạy server

```bash
# Chạy foreground (thấy log)
python3 odoo-bin.py -c odoo.conf -d tranvanlam

# Hoặc chạy background
nohup python3 odoo-bin.py -c odoo.conf -d tranvanlam > odoo.log 2>&1 &
```

### Bước 4.4: Truy cập giao diện

1. Mở trình duyệt: **http://localhost:8069**
2. Đăng nhập:
   - **Email**: `admin`
   - **Password**: `admin` (hoặc mật khẩu bạn đã đặt)

---

## 5. Cài đặt module

Sau khi đăng nhập, cài các module:

1. Vào **Cài đặt** (Settings) → **Ứng dụng** (Apps)
2. Bỏ filter "Apps" → Tìm kiếm:
   - `Quản lý nhân sự` → Nhấn **Cài đặt**
   - `Quản lý khách hàng` → Nhấn **Cài đặt**
   - `Quản lý văn bản` → Nhấn **Cài đặt**

Hoặc dùng lệnh terminal:
```bash
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -i nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init
```

---

## 6. Test Module Nhân sự (HRM)

### 6.1. Tạo đơn vị / phòng ban

1. Menu: **Nhân sự** → **Đơn vị**
2. Nhấn **Tạo**
3. Điền:
   - Tên đơn vị: `Phòng Kỹ thuật`
   - Mã đơn vị: `KT`
   - Đơn vị cha: (trống hoặc chọn đơn vị cấp trên)
4. Nhấn **Lưu**
5. ✅ **Kết quả**: Đơn vị xuất hiện trong danh sách

### 6.2. Tạo chức vụ

1. Menu: **Nhân sự** → **Chức vụ**
2. Tạo: `Trưởng phòng`, `Nhân viên`, `Giám đốc`
3. ✅ **Kết quả**: Chức vụ xuất hiện trong danh sách

### 6.3. Tạo nhân viên

1. Menu: **Nhân sự** → **Nhân viên**
2. Nhấn **Tạo**, điền đầy đủ:
   - **Thông tin cơ bản**: Họ tên, giới tính, ngày sinh, SĐT, email
   - **Công tác**: Đơn vị, chức vụ, ngày vào làm
   - **CCCD/CMND**: Số CCCD, ngày cấp, nơi cấp
   - **Địa chỉ**: Tỉnh, quận/huyện, địa chỉ chi tiết
   - **Ngân hàng**: Số tài khoản, tên ngân hàng, chi nhánh
3. Nhấn **Lưu**
4. ✅ **Kết quả**: Nhân viên được tạo với mã tự sinh (NV-XXXX)

> **Quan trọng**: Điền email nhân viên (email thật) để test email thông báo ở bước sau

### 6.4. Tạo hợp đồng lao động

1. Từ form nhân viên → Nhấn smart button **Hợp đồng** (hoặc Menu → Hợp đồng LĐ)
2. Nhấn **Tạo**:
   - Nhân viên: Chọn NV vừa tạo
   - Loại HĐ: `Xác định thời hạn`
   - Lương cơ bản: `15000000`
   - Phụ cấp: `2000000`
   - Ngày bắt đầu → Ngày kết thúc
3. Workflow: **Nháp** → Nhấn **Kích hoạt** → **Đang thực hiện**
4. ✅ **Kết quả**: HĐ chuyển sang trạng thái "Đang thực hiện", mã tự sinh HDLD-XXXX

### 6.5. Tạo đơn nghỉ phép

1. Menu: **Nhân sự** → **Nghỉ phép**
2. Nhấn **Tạo**:
   - Nhân viên: Chọn NV
   - Loại nghỉ: `Nghỉ phép năm`
   - Ngày bắt đầu → Ngày kết thúc
   - Lý do: `Nghỉ phép gia đình`
3. Nhấn **Gửi duyệt** → Trạng thái: "Chờ duyệt"
4. Nhấn **Duyệt** → Trạng thái: "Đã duyệt"
5. ✅ **Kết quả**: 
   - Đơn chuyển "Đã duyệt"
   - **📧 Email gửi cho nhân viên** (kiểm tra hộp thư)

#### Test từ chối:
1. Tạo đơn nghỉ phép mới → **Gửi duyệt**
2. Nhấn **Từ chối**
3. ✅ **Kết quả**: **📧 Email thông báo từ chối** gửi cho nhân viên

### 6.6. Tạo bảng lương

1. Menu: **Nhân sự** → **Bảng lương**
2. Nhấn **Tạo**:
   - Nhân viên: Chọn NV (có HĐ đang thực hiện)
   - Tháng/Năm: `3 / 2026`
   - Nhấn **Tính lương** → Hệ thống tự tính:
     - Lương cơ bản + phụ cấp
     - BHXH (8%), BHYT (1.5%), BHTN (1%)
     - Giảm trừ bản thân (11,000,000đ)
     - Thuế TNCN theo bậc
     - Thực lĩnh
3. Nhấn **Chi trả** → Trạng thái: "Đã chi trả"
4. ✅ **Kết quả**: **📧 Email chi tiết lương** gửi cho nhân viên

### 6.7. Tạo đánh giá KPI

1. Menu: **Nhân sự** → **Đánh giá KPI**
2. Nhấn **Tạo**:
   - Nhân viên, kỳ đánh giá (Tháng/Quý/Năm), tháng/năm
   - Điểm 5 tiêu chí (1-5): Kết quả công việc, Năng lực, Thái độ, Kỹ năng giao tiếp, Sáng tạo
3. Nhấn **Gửi đánh giá** → **Phê duyệt**
4. ✅ **Kết quả**: Điểm TB tự tính, xếp loại tự động (Xuất sắc/Tốt/Khá/TB/Yếu)

### 6.8. Tạo chương trình đào tạo

1. Menu: **Nhân sự** → **Đào tạo**
2. Nhấn **Tạo**:
   - Tên: `Khóa Python nâng cao`
   - Hình thức: `Đào tạo nội bộ`
   - Ngày bắt đầu/kết thúc, chi phí
   - Tab **Danh sách NV**: Thêm nhân viên tham gia
3. Nhấn **Lưu**
4. ✅ **Kết quả**: Chương trình đào tạo hiển thị đúng

---

## 7. Test Module CRM (Khách hàng & Bán hàng)

### 7.1. Tạo khách hàng

1. Menu: **CRM** → **Khách hàng**
2. Nhấn **Tạo**:
   - Tên KH: `Công ty ABC`
   - Loại: `Doanh nghiệp`
   - Email: `abc@company.com` (điền email thật để test)
   - SĐT, Địa chỉ, MST
3. Nhấn **Lưu**
4. ✅ **Kết quả**: KH được tạo, mã tự sinh KH-XXXX

### 7.2. Tạo cơ hội bán hàng

1. Menu: **CRM** → **Cơ hội bán hàng** (Kanban view)
2. Nhấn **Tạo** trong cột "Tiềm năng":
   - Tên: `Dự án phần mềm ABC`
   - Khách hàng: `Công ty ABC`
   - NV phụ trách: Chọn nhân viên (có email)
   - Giá trị: `50000000`
3. Kéo thả qua các giai đoạn: Tiềm năng → Thương lượng → Báo giá → Đàm phán
4. Kéo sang **Thắng**
5. ✅ **Kết quả**: 
   - Cơ hội chuyển trạng thái "Thắng"
   - **📧 Email chúc mừng** gửi cho NV phụ trách

#### Test thua:
1. Tạo cơ hội mới → Kéo sang **Thua**
2. ✅ **Kết quả**: **📧 Email thông báo thua** gửi cho NV phụ trách

### 7.3. Tạo báo giá

1. Menu: **CRM** → **Báo giá**
2. Nhấn **Tạo**:
   - Khách hàng, nhân viên, ngày báo giá, hiệu lực
   - Tab chi tiết: Thêm sản phẩm/dịch vụ, số lượng, đơn giá
3. Nhấn **Gửi khách** → **Khách duyệt**
4. ✅ **Kết quả**: Báo giá chuyển trạng thái, tổng tiền tự tính

### 7.4. Tạo hợp đồng

1. Menu: **CRM** → **Hợp đồng**
2. Nhấn **Tạo**:
   - Khách hàng, từ báo giá, giá trị, thời hạn
3. Nhấn **Kích hoạt**
4. ✅ **Kết quả**: HĐ chuyển "Đang thực hiện"

### 7.5. Tạo đơn hàng

1. Menu: **CRM** → **Đơn hàng**
2. Nhấn **Tạo**:
   - Khách hàng: `Công ty ABC`
   - Chi tiết đơn hàng: Tên SP, SL, đơn giá
3. Nhấn **Xác nhận**
4. ✅ **Kết quả**: 
   - Đơn chuyển "Đã xác nhận"
   - **📧 Email xác nhận đơn hàng** gửi cho khách hàng

5. Nhấn **Hoàn thành**
6. ✅ **Kết quả**: 
   - **📧 Email hoàn thành đơn hàng** gửi cho khách hàng

### 7.6. Tạo giao hàng

1. Menu: **CRM** → **Giao hàng**
2. Tạo phiếu giao hàng, chọn đơn hàng, địa chỉ, ngày giao
3. Cập nhật trạng thái: Đang giao → Đã giao
4. ✅ **Kết quả**: Phiếu giao hàng cập nhật

### 7.7. Tạo hóa đơn & thanh toán

1. Menu: **CRM** → **Hóa đơn** → Tạo → Xác nhận
2. Menu: **CRM** → **Thanh toán** → Tạo từ hóa đơn → Xác nhận
3. ✅ **Kết quả**: Công nợ khách hàng tự cập nhật

### 7.8. Test tính năng nâng cao

1. **Chấm điểm Lead**: CRM → Chấm điểm Lead → Kiểm tra điểm tự động
2. **Khảo sát hài lòng**: CRM → Khảo sát → Tạo khảo sát CSAT/NPS/CES
3. **Chiến dịch marketing**: CRM → Chiến dịch → Tạo và kiểm tra KPI

---

## 8. Test Module QLVB (Quản lý Văn bản)

### 8.1. Tạo loại văn bản

1. Menu: **Văn bản** → **Danh mục** → **Loại văn bản**
2. Tạo: `Công văn`, `Quyết định`, `Thông báo`, `Báo cáo`
3. ✅ **Kết quả**: Danh sách loại VB hiển thị

### 8.2. Tạo văn bản đến

1. Menu: **Văn bản** → **Văn bản đến**
2. Nhấn **Tạo**:
   - Số ký hiệu: `123/CV-ABC`
   - Nơi ban hành: `Công ty ABC`
   - Loại VB: `Công văn`
   - Trích yếu: `Về việc hợp tác kinh doanh`
   - Ngày đến, độ khẩn, hạn xử lý
   - Người xử lý: Chọn nhân viên (có email)
3. Nhấn **Tiếp nhận**
4. Nhấn **Phê duyệt**
5. ✅ **Kết quả**:
   - VB chuyển trạng thái "Đã phê duyệt"
   - **📧 Email phân công** gửi cho người xử lý

### 8.3. Tạo văn bản đi

1. Menu: **Văn bản** → **Văn bản đi**
2. Nhấn **Tạo**:
   - Số ký hiệu, loại VB, trích yếu
   - Nơi nhận, người ký
   - Người nhận email (nếu cần gửi thông báo)
3. Nhấn **Trình ký** → **Phê duyệt** → **Ban hành**
4. ✅ **Kết quả**:
   - VB chuyển "Đã ban hành"
   - **📧 Email thông báo** gửi khi phê duyệt (nếu có người nhận)

### 8.4. Sổ công văn

1. Menu: **Văn bản** → **Sổ công văn**
2. Tạo sổ: Sổ VB đến 2026, Sổ VB đi 2026
3. Mở/Khóa sổ, kiểm tra danh sách VB trong sổ
4. ✅ **Kết quả**: Sổ hiển thị đúng VB liên quan

### 8.5. Phiếu luân chuyển

1. Menu: **Văn bản** → **Phiếu luân chuyển**
2. Tạo phiếu → Chọn VB → Thêm chi tiết luân chuyển (bộ phận, thời hạn)
3. Cập nhật trạng thái từng bước
4. ✅ **Kết quả**: Lộ trình luân chuyển hiển thị đúng

### 8.6. Lưu trữ văn bản

1. Menu: **Văn bản** → **Lưu trữ**
2. Tạo hồ sơ lưu trữ → Chọn VB → Vị trí, thời hạn
3. Test: Thu hồi, Đề xuất hủy
4. ✅ **Kết quả**: Trạng thái lưu trữ cập nhật đúng

### 8.7. Luồng duyệt

1. Menu: **Văn bản** → **Cấu hình** → **Luồng duyệt**
2. Tạo luồng duyệt nhiều bước
3. Gán vào VB đi → Test phê duyệt qua từng bước
4. ✅ **Kết quả**: Lịch sử duyệt ghi nhận đầy đủ

### 8.8. Chữ ký điện tử

1. Menu: **Văn bản** → **Chữ ký điện tử**
2. Tạo chữ ký cho user (vẽ/upload)
3. Ký VB đi → Kiểm tra chữ ký hiển thị
4. ✅ **Kết quả**: Chữ ký gắn vào VB

---

## 9. Test Email thông báo

### 9.1. Cấu hình email (2 cách)

#### Cách 1: Qua file .env (khuyến nghị)

Sửa file `.env` ở gốc dự án:
```env
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

#### Cách 2: Qua giao diện Odoo

1. Menu: **Cài đặt** (Settings) → Cuộn xuống phần **Email thông báo**
2. Điền:
   - Gmail: `your-email@gmail.com`
   - App Password: `xxxx xxxx xxxx xxxx`
3. Nhấn **Lưu**

### 9.2. Checklist test email

| # | Sự kiện | Cách test | Email gửi cho |
|---|---------|-----------|---------------|
| 1 | Duyệt nghỉ phép | Tạo đơn → Gửi duyệt → Duyệt | Nhân viên |
| 2 | Từ chối nghỉ phép | Tạo đơn → Gửi duyệt → Từ chối | Nhân viên |
| 3 | Chi trả lương | Tạo bảng lương → Tính lương → Chi trả | Nhân viên |
| 4 | Xác nhận đơn hàng | Tạo đơn hàng → Xác nhận | Khách hàng |
| 5 | Hoàn thành đơn hàng | Đơn đã xác nhận → Hoàn thành | Khách hàng |
| 6 | Cơ hội thắng | Kéo cơ hội sang "Thắng" | NV phụ trách |
| 7 | Phân công VB đến | Tạo VB đến → Phê duyệt | Người xử lý |
| 8 | Phê duyệt VB đi | Tạo VB đi → Phê duyệt | Người nhận |

> **Lưu ý**: Để test email, các nhân viên/khách hàng phải có trường **email** được điền email thật

### 9.3. Kiểm tra email đã gửi

- Kiểm tra hộp thư (inbox + spam) của email người nhận
- Nếu không nhận được, kiểm tra:
  1. App Password có đúng 16 ký tự không?
  2. Gmail đã bật Xác minh 2 bước chưa?
  3. Kiểm tra log terminal Odoo: tìm dòng `Email sent successfully` hoặc lỗi SMTP

---

## 10. Test Báo cáo nâng cao

### 10.1. Calendar View (Lịch)

| View | Cách truy cập | Kiểm tra |
|------|---------------|----------|
| Lịch nghỉ phép | Nhân sự → Nghỉ phép → Icon Calendar | Hiện đơn nghỉ theo ngày, màu theo loại nghỉ |
| Lịch đào tạo | Nhân sự → Đào tạo → Icon Calendar | Hiện khóa đào tạo theo ngày bắt đầu/kết thúc |
| Lịch VB đến | Văn bản → VB đến → Icon Calendar | Hiện VB theo ngày đến, màu theo độ khẩn |
| Lịch luân chuyển | Văn bản → Luân chuyển → Icon Calendar | Hiện phiếu theo ngày tạo |

### 10.2. Pivot View (Bảng phân tích)

| View | Cách truy cập | Kiểm tra |
|------|---------------|----------|
| Pivot bảng lương | Nhân sự → Bảng lương → Icon Pivot | Bảng: Đơn vị × Tháng = Thực lĩnh |
| Pivot KPI | Nhân sự → KPI → Icon Pivot | Bảng: Đơn vị × Kỳ = Điểm TB |
| Pivot đơn hàng | CRM → Đơn hàng → Icon Pivot | Bảng: KH × Trạng thái = Tổng tiền |
| Pivot cơ hội | CRM → Cơ hội → Icon Pivot | Bảng: NV × Giai đoạn = Giá trị |
| Pivot VB đến | Văn bản → VB đến → Icon Pivot | Bảng: Loại VB × Trạng thái |
| Pivot VB đi | Văn bản → VB đi → Icon Pivot | Bảng: Loại VB × Trạng thái |

### 10.3. Graph View (Biểu đồ)

| View | Cách truy cập | Kiểm tra |
|------|---------------|----------|
| Biểu đồ lương | Nhân sự → Bảng lương → Icon Graph | Cột: Thu nhập/Thực lĩnh theo NV |
| Biểu đồ KPI | Nhân sự → KPI → Icon Graph | Cột: Điểm TB theo NV |
| Biểu đồ đơn hàng | CRM → Đơn hàng → Icon Graph | Bar + Line: Doanh thu theo trạng thái |
| Biểu đồ cơ hội | CRM → Cơ hội → Icon Graph (list view) | Bar: Giá trị theo giai đoạn |
| Biểu đồ thanh toán | CRM → Thanh toán → Icon Graph | Pie: Theo hình thức thanh toán |
| Biểu đồ VB đến | Văn bản → VB đến → Icon Graph | Bar + Pie: Trạng thái, Độ khẩn |
| Biểu đồ VB đi | Văn bản → VB đi → Icon Graph | Bar: Theo trạng thái |

---

## 11. Test Chatbot AI

### 11.1. Truy cập chatbot

1. Menu: **Văn bản** → **Chatbot AI** hoặc tìm menu chatbot
2. Giao diện chat mở ra

### 11.2. Test các tình huống

| # | Câu hỏi test | Kết quả mong đợi |
|---|-------------|-----------------|
| 1 | `Xin chào` | Chatbot chào hỏi |
| 2 | `Hướng dẫn tạo văn bản đi` | Hướng dẫn chi tiết các bước |
| 3 | `Có bao nhiêu văn bản đến trong tháng này?` | Trả lời dựa trên data hệ thống |
| 4 | `Giải thích quy trình luân chuyển văn bản` | Mô tả quy trình |
| 5 | Câu tiếng Anh: `How to create an incoming document?` | Trả lời bằng Anh/Việt |

### 11.3. Xử lý lỗi chatbot

- Nếu chatbot không phản hồi → Kiểm tra `GEMINI_API_KEY` trong `.env`
- Nếu lỗi 429 → API rate limit, đợi 1 phút thử lại
- Nếu lỗi 400 → Key không hợp lệ, tạo key mới

---

## 12. Lệnh cập nhật module

### Cập nhật code mới (khi sửa code)

```bash
# Dừng server đang chạy
pkill -f "odoo-bin"

# Cập nhật 3 module
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -u nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init

# Khởi chạy lại
nohup python3 odoo-bin.py -c odoo.conf -d tranvanlam > odoo.log 2>&1 &
```

### Cập nhật 1 module cụ thể

```bash
python3 odoo-bin.py -c odoo.conf -d tranvanlam -u nhan_su --stop-after-init
```

### Xem log realtime

```bash
tail -f odoo.log
```

---

## 13. Xử lý lỗi thường gặp

### Lỗi 1: `Cannot import name 'x509' from 'cryptography'`

```bash
pip install cryptography==41.0.7 pyOpenSSL==23.3.0
```

### Lỗi 2: PostgreSQL connection refused

```bash
# Kiểm tra Docker container
docker ps
# Nếu không thấy, khởi động lại
docker-compose up -d
```

### Lỗi 3: Port 8069 đã bị chiếm

```bash
# Tìm process đang dùng port
lsof -i :8069
# Hoặc kill process Odoo cũ
pkill -f "odoo-bin"
```

### Lỗi 4: Email không gửi được

1. Kiểm tra `.env`:
   - `GMAIL_APP_PASSWORD` phải là **App Password 16 ký tự** (không phải mật khẩu Gmail thường)
   - Gmail phải bật **Xác minh 2 bước**
2. Kiểm tra email nhân viên/khách hàng có được điền không
3. Xem log Odoo tìm lỗi SMTP

### Lỗi 5: Chatbot không phản hồi

1. Kiểm tra `GEMINI_API_KEY` trong `.env`
2. Thử gọi API trực tiếp:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Lỗi 6: Module không tìm thấy

```bash
# Kiểm tra addons_path trong odoo.conf chỉ đúng thư mục
# Đảm bảo mỗi module có file __manifest__.py
ls addons/nhan_su/__manifest__.py
ls addons/quan_ly_khach_hang/__manifest__.py
ls addons/quan_ly_van_ban/__manifest__.py
```

### Lỗi 7: Lỗi `KeyNotFoundError` khi cài module

```bash
# Reset database và cài lại
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -u nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init
```

---

## 14. Quy trình test hoàn chỉnh (Checklist)

### Phase 1: Chuẩn bị
- [ ] Docker PostgreSQL đang chạy (`docker ps`)
- [ ] File `.env` đã cấu hình API key + Gmail
- [ ] 3 module đã cài đặt thành công
- [ ] Server Odoo đang chạy (http://localhost:8069)

### Phase 2: Dữ liệu cơ sở
- [ ] Tạo 2-3 đơn vị
- [ ] Tạo 3-4 chức vụ
- [ ] Tạo 3-5 nhân viên (có email thật)
- [ ] Tạo 2-3 khách hàng (có email thật)
- [ ] Tạo các loại văn bản

### Phase 3: Test HRM
- [ ] Tạo hợp đồng lao động → Kích hoạt
- [ ] Tạo đơn nghỉ phép → Duyệt → ✅ Nhận email
- [ ] Tạo đơn nghỉ phép → Từ chối → ✅ Nhận email
- [ ] Tạo bảng lương → Tính lương → Chi trả → ✅ Nhận email
- [ ] Tạo đánh giá KPI → Phê duyệt
- [ ] Tạo chương trình đào tạo

### Phase 4: Test CRM
- [ ] Tạo cơ hội → Kéo qua pipeline → Thắng → ✅ Nhận email
- [ ] Tạo cơ hội → Thua → ✅ Nhận email
- [ ] Tạo báo giá → Gửi → Duyệt
- [ ] Tạo đơn hàng → Xác nhận → ✅ Nhận email
- [ ] Đơn hàng → Hoàn thành → ✅ Nhận email
- [ ] Tạo giao hàng → Cập nhật trạng thái
- [ ] Tạo hóa đơn → Thanh toán → Kiểm tra công nợ

### Phase 5: Test QLVB
- [ ] Tạo VB đến → Tiếp nhận → Phê duyệt → ✅ Nhận email
- [ ] Tạo VB đi → Trình ký → Phê duyệt → Ban hành → ✅ Nhận email
- [ ] Tạo sổ công văn → Mở/Khóa
- [ ] Tạo phiếu luân chuyển → Cập nhật
- [ ] Tạo hồ sơ lưu trữ
- [ ] Test chatbot AI → Nhận phản hồi

### Phase 6: Test Views nâng cao
- [ ] Kiểm tra 4 Calendar views
- [ ] Kiểm tra 6+ Pivot views
- [ ] Kiểm tra 7+ Graph views
- [ ] Kiểm tra Dashboard từng module

### Phase 7: Test Settings
- [ ] Cấu hình Gmail trong Cài đặt → Lưu → Hoạt động

---

> **Ghi chú**: Tổng cộng có **~35 test cases** cần kiểm tra. Thời gian test toàn bộ tùy thuộc vào kinh nghiệm. Nên test theo thứ tự Phase 1 → 7 để đảm bảo dữ liệu đầy đủ cho các bước sau.
