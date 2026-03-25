# HƯỚNG DẪN TEST — ERP: Quản lý Nhân sự – Khách hàng – Văn bản

> **Dự án**: CNTT17-07-NHOM4  
> **Nền tảng**: Odoo 15.0 (Community) · Python 3.10 · PostgreSQL 10 (Docker)  
> **Hệ điều hành**: Ubuntu 20.04+ / WSL2  
> **Cập nhật**: 25/03/2026

---

## MỤC LỤC

1. [Yêu cầu môi trường](#1-yêu-cầu-môi-trường)
2. [Cài đặt và khởi động](#2-cài-đặt-và-khởi-động)
3. [Cài đặt module](#3-cài-đặt-module)
4. [Test Module Nhân sự (nhan_su)](#4-test-module-nhân-sự-nhan_su)
5. [Test Module CRM / Khách hàng (quan_ly_khach_hang)](#5-test-module-crm--khách-hàng-quan_ly_khach_hang)
6. [Test Module Văn bản (quan_ly_van_ban)](#6-test-module-văn-bản-quan_ly_van_ban)
7. [Test Tích hợp liên module](#7-test-tích-hợp-liên-module)
8. [Test Email Gmail](#8-test-email-gmail)
9. [Test Chatbot AI Gemini](#9-test-chatbot-ai-gemini)
10. [Checklist tổng hợp](#10-checklist-tổng-hợp)

---

## 1. Yêu cầu môi trường

| Thành phần | Phiên bản | Ghi chú |
|---|---|---|
| Python | 3.10.x | Bắt buộc đúng 3.10 |
| PostgreSQL | 10 (Docker) | Chạy qua docker-compose, port **5431** |
| Docker | 20.10+ | Docker Compose v3.5 |
| RAM | ≥ 4 GB | Odoo + PostgreSQL |
| Gmail App Password | 16 ký tự | Dùng cho thông báo email |
| Gemini API Key | — | Google AI Studio |

---

## 2. Cài đặt và khởi động

### 2.1 Clone và thiết lập môi trường ảo

```bash
cd /home/$USER
git clone <repo-url> CNTT17-07-NHOM4
cd CNTT17-07-NHOM4

# Cài thư viện hệ thống
sudo apt-get update && sudo apt-get install -y \
  libxml2-dev libxslt-dev libldap2-dev libsasl2-dev \
  libssl-dev python3.10-distutils python3.10-dev \
  build-essential libffi-dev zlib1g-dev python3.10-venv libpq-dev

# Tạo và kích hoạt venv
python3.10 -m venv venv
source venv/bin/activate

# Cài Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install cryptography==41.0.7 pyOpenSSL==23.3.0 urllib3==1.26.18
```

### 2.2 Khởi động PostgreSQL

```bash
# Trong thư mục gốc dự án
sudo docker-compose up -d

# Xác nhận container đang chạy
sudo docker ps | grep postgres_odoo
```

Kết quả mong đợi: container `postgres_odoo-base-15-01` ở trạng thái **Up**.

### 2.3 Tạo file cấu hình

**`odoo.conf`** — nên dùng file mẫu sẵn có:
```bash
cp odoo.conf.template odoo.conf
# Kiểm tra: db_port = 5431, db_user = odoo, db_password = odoo
```

**`.env`** — API keys (nếu chưa có):
```bash
cat > .env << 'EOF'
GEMINI_API_KEY=<your-gemini-api-key>
GMAIL_EMAIL=<your-email@gmail.com>
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
EOF
```

> **Lưu ý**: File `.env` đã có sẵn với key thật. Không commit file này lên Git.

### 2.4 Xác nhận kết nối database

```bash
source venv/bin/activate
python3 odoo-bin.py shell -c odoo.conf --stop-after-init 2>&1 | tail -5
```

---

## 3. Cài đặt module

### Cài lần đầu (database mới)

```bash
source venv/bin/activate
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -i nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init
```

Thời gian ước tính: **3–7 phút** (tùy phần cứng).

### Khởi động server

```bash
python3 odoo-bin.py -c odoo.conf -d tranvanlam
```

Truy cập: **http://localhost:8069**  
Đăng nhập: `admin` / `admin`

### Cập nhật module (khi thay đổi code)

```bash
# Dừng server (Ctrl+C), rồi chạy:
python3 odoo-bin.py -c odoo.conf -d tranvanlam \
  -u nhan_su,quan_ly_khach_hang,quan_ly_van_ban \
  --stop-after-init
python3 odoo-bin.py -c odoo.conf -d tranvanlam
```

---

## 4. Test Module Nhân sự (`nhan_su`)

### 4.1 Quản lý danh mục

**Menu**: `Nhân sự → Danh mục`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo **Đơn vị / Phòng ban**: tên "Phòng Kỹ thuật", cấp độ 2 | Lưu thành công, hiển thị trong danh sách |
| 2 | Tạo **Chức vụ**: tên "Kỹ sư phần mềm", cấp độ 3 | Lưu thành công |
| 3 | Xem danh sách đơn vị → Tree view | Bảng danh sách phân cấp |

### 4.2 Quản lý nhân viên

**Menu**: `Nhân sự → Nhân viên`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo nhân viên mới: Họ tên, CCCD (12 số), ngày sinh, phòng ban, chức vụ | Lưu thành công, sidebar chính xác |
| 2 | Tải ảnh đại diện | Ảnh hiển thị trong form |
| 3 | Chuyển sang tab "Thông tin ngân hàng", nhập số TK | Lưu thành công |
| 4 | Xem Kanban view | Card nhân viên với ảnh, tên, phòng ban |
| 5 | Tìm kiếm theo tên | Lọc đúng kết quả |

### 4.3 Hợp đồng lao động

**Menu**: `Nhân sự → Hợp đồng lao động`

Workflow: **Dự thảo → Hiệu lực → Chấm dứt**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo HĐLĐ: chọn nhân viên, loại HĐ "Không xác định thời hạn", lương cơ bản 15,000,000 | Tạo thành công, trạng thái "Dự thảo" |
| 2 | Nhập phụ cấp, các khoản thưởng | Trường `tong_thu_nhap` tự tính |
| 3 | Nhấn **"Kích hoạt"** | Chuyển sang "Hiệu lực" |
| 4 | Nhấn **"Chấm dứt"** (nếu cần) | Chuyển sang "Chấm dứt" |
| 5 | Cron tự động hết hạn | HĐ có thời hạn tự chuyển trạng thái sau ngày hết hạn |

### 4.4 Nghỉ phép

**Menu**: `Nhân sự → Nghỉ phép`

Workflow: **Nháp → Chờ duyệt → Đã duyệt / Từ chối / Đã hủy**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo đơn: loại "Phép năm", từ ngày, đến ngày, lý do | Mã đơn tự sinh (NP/...) |
| 2 | Nhấn **"Gửi duyệt"** | Chuyển "Chờ duyệt" |
| 3 | Nhấn **"Duyệt"** | Trạng thái "Đã duyệt" + email gửi cho nhân viên |
| 4 | Tạo đơn khác → Nhấn **"Từ chối"** + nhập lý do | Trạng thái "Từ chối" |
| 5 | Kiểm tra Calendar view | Lịch nghỉ phép hiển thị |

### 4.5 Bảng lương

**Menu**: `Nhân sự → Bảng lương`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo bảng lương tháng 3/2026: chọn nhân viên | Form mở |
| 2 | Nhập ngày công thực tế, số ngày công chuẩn | Lương thực nhận tự tính |
| 3 | Kiểm tra: BHXH (8%), BHYT (1.5%), BHTN (1%), thuế TNCN 7 bậc | Các khoản khấu trừ đúng |
| 4 | Nhấn **"Chi trả"** | Trạng thái "Đã chi trả" + email thông báo |
| 5 | Xem Pivot view | Tổng lương theo phòng ban/tháng |

### 4.6 Đánh giá KPI

**Menu**: `Nhân sự → Đánh giá KPI`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo đánh giá: chọn nhân viên, kỳ "Tháng 3/2026" | Form mở |
| 2 | Nhập điểm 5 tiêu chí (thang 1–5) | Điểm tổng tự tính |
| 3 | Kiểm tra xếp loại tự động | Xuất sắc (≥4.5) / Tốt / Khá / TB / Yếu |
| 4 | Xem Graph view | Biểu đồ điểm KPI |

### 4.7 Đào tạo

**Menu**: `Nhân sự → Đào tạo`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo khoá đào tạo: tên, hình thức, chi phí, ngày bắt đầu–kết thúc | Lưu thành công |
| 2 | Thêm danh sách nhân viên tham gia | Hiển thị đúng số người |
| 3 | Xem Calendar view | Khoá đào tạo hiển thị trên lịch |

### 4.8 Dashboard nhân sự

**Menu**: `Nhân sự → Dashboard`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở Dashboard | Widget tổng số NV, NV đang làm, NV nghỉ hiển thị |
| 2 | Kiểm tra biểu đồ | Chart.js render đúng |

---

## 5. Test Module CRM / Khách hàng (`quan_ly_khach_hang`)

### 5.1 Quản lý khách hàng

**Menu**: `Khách hàng → Khách hàng`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo KH cá nhân: họ tên, SĐT, email, địa chỉ | Mã KH tự sinh |
| 2 | Tạo KH doanh nghiệp: tên công ty, MST, người liên hệ | Lưu thành công |
| 3 | Phân tầng KH: "Vàng" | Cập nhật hiển thị trên card |
| 4 | Xem Kanban view | Card KH với thông tin tóm tắt |

### 5.2 Pipeline cơ hội bán hàng

**Menu**: `Khách hàng → Cơ hội bán hàng`

Workflow: **Mới → Đủ điều kiện → Đang báo giá → Đàm phán → Thắng / Thua**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo cơ hội: tên, KH, nguồn "Website", giá trị 100M VND, ngày dự kiến chốt | Tạo thành công, giai đoạn "Mới" |
| 2 | Nhấn **"Chuyển giai đoạn"** ×3 | Tiến lên "Đàm phán" |
| 3 | Nhấn **"Đánh dấu Thắng"** | Giai đoạn "Thắng", trạng thái "Đã thắng" + email |
| 4 | Kiểm tra biểu đồ Funnel | Số cơ hội mỗi giai đoạn đúng |
| 5 | Tạo báo giá từ cơ hội (nút "Tạo báo giá") | Báo giá liên kết với cơ hội |

### 5.3 Báo giá

**Menu**: `Khách hàng → Báo giá`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở báo giá vừa tạo, thêm sản phẩm/dịch vụ + đơn giá + số lượng | Tổng tiền tự tính |
| 2 | Nhấn **"Khách đồng ý"** | Trạng thái cập nhật |
| 3 | Nhấn **"Tạo hợp đồng"** | Form hợp đồng liên kết sẵn thông tin |

### 5.4 Hợp đồng bán hàng & Chữ ký điện tử

**Menu**: `Khách hàng → Hợp đồng`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở hợp đồng, bổ sung điều khoản, giá trị | Lưu thành công |
| 2 | Nhấn **"Ký hợp đồng"** → wizard chữ ký mở | Wizard hiển thị đúng |
| 3 | Upload file chữ ký (PNG) + nhập mã xác nhận | Hợp đồng được đánh dấu đã ký |

### 5.5 Đơn hàng → Giao hàng → Hóa đơn → Thanh toán

**Menu**: `Khách hàng → Đơn hàng`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo đơn hàng từ cơ hội (hoặc trực tiếp): chọn KH, thêm sản phẩm | Mã đơn hàng tự sinh |
| 2 | Nhấn **"Xác nhận đơn"** | Trạng thái "Đã xác nhận" + email KH |
| 3 | Chuyển sang tab Giao hàng → Nhấn **"Xác nhận giao hàng"** | Phiếu giao hàng tạo |
| 4 | Tạo hóa đơn từ đơn hàng | Hóa đơn liên kết |
| 5 | Tạo thanh toán | Trạng thái "Đã thanh toán" + email |
| 6 | Kiểm tra công nợ khách hàng | Dashboard công nợ cập nhật |

### 5.6 Chấm điểm Lead

**Menu**: `Khách hàng → Chấm điểm Lead`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo bản ghi chấm điểm cho KH | Form mở |
| 2 | Nhập các tiêu chí (tương tác, ngân sách, thời gian...) | Điểm 0–100 tự tính |
| 3 | Kiểm tra xếp hạng | Hot (≥75) / Warm / Cold / Frozen |

### 5.7 Chiến dịch marketing & Khảo sát

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo chiến dịch: loại "Email Marketing", ngân sách, lọc KH | Tạo thành công |
| 2 | Tạo khảo sát hài lòng cho KH đã mua: loại CSAT | Điểm hài lòng lưu |
| 3 | Xem Pivot view chiến dịch | ROI, tỷ lệ phản hồi |

### 5.8 Dashboard CRM

**Menu**: `Khách hàng → Dashboard`

| Kết quả mong đợi |
|---|
| Widget: Tổng doanh thu, Số cơ hội, Số KH, Đơn hàng tháng này |
| Biểu đồ Chart.js render đúng |

---

## 6. Test Module Văn bản (`quan_ly_van_ban`)

### 6.1 Danh mục loại văn bản

**Menu**: `Văn bản → Danh mục → Loại văn bản`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo loại văn bản: "Quyết định", mã "QD" | Lưu thành công |
| 2 | Tạo thêm: "Công văn", "Thông báo", "Hợp đồng" | Đủ danh mục |

### 6.2 Sổ công văn

**Menu**: `Văn bản → Sổ công văn`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo sổ VB đến 2026: loại "Đến", năm 2026 | Trạng thái "Mở" |
| 2 | Tạo sổ VB đi 2026: loại "Đi", năm 2026 | Trạng thái "Mở" |
| 3 | Khóa sổ cũ (2025 nếu có) | Trạng thái "Khóa", không thêm VB được |

### 6.3 Văn bản đến

**Menu**: `Văn bản → Văn bản đến`

Workflow: **Mới → Đang xử lý → Đã xử lý / Quá hạn / Chuyển tiếp**

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo VBĐ: số ký hiệu "CV-001/2026", loại, đơn vị gửi, ngày đến, độ khẩn "Khẩn", hạn xử lý 5 ngày | Mã tự sinh, trạng thái "Mới" |
| 2 | Upload file đính kèm (PDF) | File lưu thành công |
| 3 | Phân công người xử lý → nhấn **"Phân công"** | Trạng thái "Đang xử lý" + email người xử lý |
| 4 | Nhấn **"Đánh dấu đã xử lý"** | Trạng thái "Đã xử lý" |
| 5 | Kiểm tra Calendar view | VBĐ hiển thị theo hạn xử lý |
| 6 | Kiểm tra cron quá hạn | VBĐ hết hạn tự chuyển "Quá hạn" |

### 6.4 Văn bản đi

**Menu**: `Văn bản → Văn bản đi`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo VBĐi: số ký hiệu, loại, đơn vị nhận, nội dung tóm tắt | Lưu thành công |
| 2 | Chọn luồng duyệt (nếu có cấu hình) | Luồng duyệt áp dụng |
| 3 | Nhấn **"Gửi ký"** / upload chữ ký | Trạng thái cập nhật |
| 4 | Nhấn **"Phát hành"** | VBĐi đã gửi + email thông báo KH (nếu có) |

### 6.5 Luồng duyệt đa cấp

**Menu**: `Văn bản → Luồng duyệt`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo luồng duyệt "Duyệt hợp đồng": 3 bước, mỗi bước chỉ định người duyệt | Lưu thành công |
| 2 | Áp luồng vào VB đi | Bước duyệt hiển thị |
| 3 | Người duyệt B1 xác nhận | Chuyển B2 |
| 4 | Người duyệt cuối ký duyệt | Hoàn tất luồng |

### 6.6 Chữ ký điện tử

**Menu**: `Văn bản → Chữ ký điện tử`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở VB đi → Nhấn **"Ký điện tử"** | Wizard upload mở |
| 2 | Upload file chữ ký + nhập thông tin | Hash được tạo và lưu |
| 3 | Xem lịch sử audit trail | Ghi nhận thời gian, người ký, hash |

### 6.7 OCR văn bản

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Upload file PDF/ảnh trong form VBĐ | File lưu |
| 2 | Nhấn **"Trích xuất OCR"** (nếu có nút) | Nội dung text điền vào trường tóm tắt |

### 6.8 Lưu trữ văn bản

**Menu**: `Văn bản → Lưu trữ`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo phiếu lưu trữ: VB, tủ/kệ/ngăn, thời hạn lưu | Lưu thành công |
| 2 | Đề xuất hủy VB hết hạn lưu | Trạng thái "Đề xuất hủy" |

### 6.9 Phiếu luân chuyển

**Menu**: `Văn bản → Luân chuyển`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo phiếu luân chuyển từ VBĐ → Phòng Kỹ thuật | Phiếu tạo thành công |
| 2 | Phòng nhận xác nhận tiếp nhận | Bước luân chuyển ghi nhận |
| 3 | Xem lịch sử luân chuyển | Mỗi bước có thời gian và người xử lý |

### 6.10 Dashboard văn bản

**Menu**: `Văn bản → Dashboard`

| Kết quả mong đợi |
|---|
| Số VB đến theo trạng thái, VB quá hạn |
| Số VB đi chờ ký, đã phát hành |
| Biểu đồ theo tháng/loại |

### 6.11 Mẫu văn bản

**Menu**: `Văn bản → Mẫu văn bản`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Tạo mẫu: tên "Mẫu quyết định", nội dung Jinja2 | Lưu thành công |
| 2 | Sinh VB từ mẫu | VB tự điền nội dung theo template |

---

## 7. Test Tích hợp liên module

### 7.1 HRM → CRM

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở cơ hội bán hàng → trường "Nhân viên phụ trách" | Dropdown hiển thị danh sách `nhan_vien` |
| 2 | Chọn NV phụ trách | Lưu thành công, liên kết đúng |
| 3 | Mở đơn hàng → trường "Nhân viên phụ trách" | Tương tự |

### 7.2 HRM → Văn bản

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở VBĐ → "Người xử lý" | Chọn từ `nhan_vien` |
| 2 | Mở luồng duyệt → "Người duyệt bước 1" | Chọn từ `nhan_vien` |

### 7.3 CRM → Văn bản (tự động tạo VBĐ)

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Trong cơ hội bán hàng → tạo hợp đồng | Form hợp đồng CRM mở |
| 2 | Lưu hợp đồng CRM | VBĐi trong module Văn bản tự sinh liên kết hợp đồng |
| 3 | Kiểm tra VBĐi trong Văn bản | `hop_dong_id` / `co_hoi_id` điền đúng |

### 7.4 Email service tập trung (nhan_su → cả 3 module)

| Module | Sự kiện | Email gửi đến |
|---|---|---|
| nhan_su | Duyệt nghỉ phép | Nhân viên xin nghỉ |
| nhan_su | Chi trả bảng lương | Nhân viên được chi trả |
| quan_ly_khach_hang | Thắng cơ hội | Nhân viên phụ trách |
| quan_ly_khach_hang | Xác nhận đơn hàng | Khách hàng |
| quan_ly_khach_hang | Hoàn thành đơn hàng | Khách hàng |
| quan_ly_van_ban | Phân công VBĐ | Người xử lý |
| quan_ly_van_ban | Phát hành VBĐi | Khách hàng liên quan |

---

## 8. Test Email Gmail

### 8.1 Cấu hình

**Menu**: `Nhân sự → Cài đặt → Cấu hình Email Gmail`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Nhập Gmail + App Password (16 ký tự, đọc từ `.env`) | Lưu thành công |
| 2 | Nhấn **"Kiểm tra kết nối"** | Thông báo "Kết nối thành công!" |

### 8.2 Gửi email thực

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Duyệt đơn nghỉ phép có email NV | Email đến inbox NV trong ≤2 phút |
| 2 | Chi trả bảng lương | Email thông báo lương gửi đến NV |
| 3 | Xác nhận đơn hàng có KH email | Email đến inbox KH |

> **Lưu ý**: Nếu không nhận email, kiểm tra Spam và cấu hình Gmail SMTP.

---

## 9. Test Chatbot AI Gemini

**Menu**: `Văn bản → Chatbot AI` (icon chat góc màn hình)

### 9.1 Kiểm tra kết nối Gemini

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở chatbot | Widget chat hiển thị, trạng thái "Sẵn sàng" |
| 2 | Gõ: `"Xin chào"` | Bot phản hồi trong <5 giây |

### 9.2 Câu hỏi nghiệp vụ hệ thống

| Câu hỏi | Kết quả mong đợi |
|---|---|
| `"Danh sách nhân viên phòng Kỹ thuật"` | Liệt kê NV đúng |
| `"Có bao nhiêu văn bản đến chưa xử lý?"` | Số VB đang xử lý |
| `"Cơ hội bán hàng tháng này"` | Tóm tắt pipeline |
| `"Tổng doanh thu quý 1 năm 2026"` | Tra cứu và hiển thị số liệu |
| `"Văn bản nào sắp quá hạn xử lý?"` | Danh sách VB gần deadline |

### 9.3 Xem lịch sử hội thoại

**Menu**: `Văn bản → Lịch sử chat`

| Bước | Thao tác | Kết quả mong đợi |
|---|---|---|
| 1 | Mở lịch sử | Các cuộc hội thoại theo session |
| 2 | Tìm kiếm theo nội dung | Filter đúng |

---

## 10. Checklist tổng hợp

### Module `nhan_su`

- [ ] Tạo phòng ban, chức vụ
- [ ] Tạo nhân viên đầy đủ thông tin
- [ ] Tạo và kích hoạt hợp đồng lao động
- [ ] Xin và duyệt nghỉ phép → email gửi
- [ ] Tạo bảng lương → chi trả → email gửi
- [ ] Đánh giá KPI với điểm ≥ 4.5 → xếp loại "Xuất sắc"
- [ ] Tạo khoá đào tạo → xem Calendar
- [ ] Dashboard hiển thị đúng số liệu

### Module `quan_ly_khach_hang`

- [ ] Tạo KH cá nhân và doanh nghiệp
- [ ] Tạo cơ hội → chuyển giai đoạn → Thắng → email
- [ ] Báo giá → KH đồng ý → tạo hợp đồng → ký
- [ ] Đơn hàng → Xác nhận → Giao hàng → Hóa đơn → Thanh toán → email
- [ ] Lead scoring: điểm 80 → xếp "Hot"
- [ ] Dashboard CRM hiển thị đúng số liệu

### Module `quan_ly_van_ban`

- [ ] Tạo sổ công văn đến/đi 2026
- [ ] Tạo VBĐ → phân công → xử lý → email
- [ ] Tạo VBĐi → duyệt → ký điện tử → phát hành
- [ ] Luồng duyệt 3 bước hoạt động đúng
- [ ] Phiếu luân chuyển ghi nhận từng bước
- [ ] Lưu trữ vật lý với tủ/kệ/ngăn
- [ ] Dashboard văn bản hiển thị đúng

### Tích hợp

- [ ] NV phụ trách cơ hội bán hàng lấy từ `nhan_vien`
- [ ] VBĐi tự sinh từ hợp đồng CRM
- [ ] Email service tập trung hoạt động cho cả 3 module
- [ ] Chatbot trả lời câu hỏi nghiệp vụ đúng

---

> **Ghi chú**: Nếu gặp lỗi `Module not found` hoặc `ImportError`, chạy lại lệnh cập nhật module với flag `-u`. Nếu lỗi cơ sở dữ liệu, kiểm tra container Docker đang chạy (`sudo docker ps`).
