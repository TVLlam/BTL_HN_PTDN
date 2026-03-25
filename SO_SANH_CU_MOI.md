# SO SÁNH PHIÊN BẢN CŨ → MỚI — ERP: Quản lý Nhân sự – Khách hàng – Văn bản

> **Nhóm**: CNTT17-07 — Nhóm 4  
> **Nền tảng**: Odoo 15.0 Community · Python 3.10 · PostgreSQL 10  
> **Cập nhật**: 25/03/2026

---

## 1. Tổng quan kiến trúc

| Tiêu chí | Phiên bản cũ | Phiên bản mới (hiện tại) |
|---|---|---|
| **Cấu trúc module** | 1 addon tổng hợp, code lẫn lộn | **3 addon độc lập**: `nhan_su`, `quan_ly_khach_hang`, `quan_ly_van_ban` |
| **Phụ thuộc** | Không phân tầng rõ | `nhan_su` → `quan_ly_khach_hang` → `quan_ly_van_ban` (phân tầng rõ ràng) |
| **Email** | Mỗi module tự gửi riêng | **Email service tập trung** tại `nhan_su/models/email_service.py`, dùng chung |
| **AI / Chatbot** | Không có | **Chatbot Gemini 2.5 Flash** tích hợp vào module văn bản |
| **Frontend** | XML view cơ bản | OWL JS + Chart.js + Dashboard widget tùy chỉnh |
| **Database** | SQLite / PostgreSQL đơn giản | PostgreSQL 10 (Docker), port 5431 |

---

## 2. Module Nhân sự (`nhan_su`)

### 2.1 Model & dữ liệu

| Model | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| `nhan_vien` | ~10 trường cơ bản | **50+ trường**: CCCD, trình độ, ngân hàng, trạng thái làm việc, ảnh |
| `don_vi` | Tên đơn vị đơn giản | Cấp độ phân cấp, mã đơn vị |
| `chuc_vu` | Tên chức vụ | Cấp độ chức vụ, mã chức vụ |
| `hop_dong_lao_dong` | Chỉ lưu lương cơ bản | 4 loại HĐ, phụ cấp, compute `tong_thu_nhap`, workflow 3 trạng thái, cron tự động |
| `nghi_phep` | Chỉ ghi nhận ngày | **7 loại nghỉ**, workflow 5 trạng thái, số ngày tự tính, **email thông báo** |
| `bang_luong` | Nhập tay | BHXH/BHYT/BHTN tự tính, **thuế TNCN 7 bậc**, giảm trừ gia cảnh, **email chi trả** |
| `danh_gia_kpi` | Không có | **5 tiêu chí** (1–5), tự phân loại 5 mức, kỳ tháng/quý/năm |
| `dao_tao` | Không có | 4 hình thức, chi phí, danh sách NV, Calendar view |
| `lich_su_cong_tac` | Không có | Lịch sử điều động, thuyên chuyển toàn bộ |
| `chung_chi_bang_cap` | Không có | Quản lý chứng chỉ, bằng cấp kèm file scan |
| `email_service` | Không có | **Dịch vụ email Gmail SMTP tập trung** cho toàn hệ thống |
| `dashboard` | Không có | **Dashboard OWL** thống kê tổng số NV, trạng thái, biểu đồ Chart.js |

### 2.2 Views

| View | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Form | Đơn giản, ít tab | Multi-tab, tab ngân hàng, tab hồ sơ |
| Tree | Cơ bản | Có màu trạng thái, widget badge |
| Kanban | Không có | Card với ảnh, phòng ban, chức vụ |
| Graph | Không có | Biểu đồ lương, KPI theo phòng ban |
| Calendar | Không có | Calendar cho nghỉ phép, đào tạo |
| Pivot | Không có | Pivot cho lương, KPI |
| Dashboard | Không có | Custom OWL widget |

---

## 3. Module CRM / Khách hàng (`quan_ly_khach_hang`)

### 3.1 Model & dữ liệu

| Model | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| `khach_hang` | Thông tin cơ bản | Cá nhân/doanh nghiệp, phân tầng (Đồng→Kim cương), mã tự sinh |
| `co_hoi_ban_hang` | Không có | Pipeline **6 giai đoạn**, ty lệ thành công, giá trị dự kiến, **email thắng/thua** |
| `bao_gia` | Không có | Báo giá chi tiết, workflow KH đồng ý/từ chối, liên kết cơ hội |
| `hop_dong` | Lưu trữ đơn giản | Workflow duyệt, **chữ ký điện tử** (upload + hash), liên kết VB |
| `don_hang` + `don_hang_chi_tiet` | Không có | Đơn hàng với sản phẩm/dịch vụ, **email xác nhận/hoàn thành** |
| `giao_hang` | Không có | Phiếu giao hàng, wizard xác nhận |
| `hoa_don` | Không có | Hóa đơn bán hàng liên kết đơn hàng |
| `thanh_toan` | Không có | Đa hình thức thanh toán, **email xác nhận** |
| `cong_no_khach_hang` | Không có | Dashboard công nợ, theo dõi dư nợ |
| `co_hoi_ban_hang` | Không có | Lead scoring 0–100, phân loại Hot/Warm/Cold/Frozen |
| `chien_dich_marketing` | Không có | 7 loại chiến dịch, lọc KH, KPI ROI |
| `khao_sat_hai_long` | Không có | CSAT/NPS/CES |
| `loyalty_program` | Không có | Chương trình thân thiết, tích điểm |
| `khieu_nai_phan_hoi` | Không có | Khiếu nại, SLA, mức ưu tiên |

### 3.2 Tích hợp

| Luồng | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Cơ hội → Báo giá | Thủ công | Nút "Tạo báo giá" trực tiếp từ cơ hội |
| Báo giá → Hợp đồng | Thủ công | Nút "Tạo hợp đồng" từ báo giá đã được duyệt |
| Hợp đồng → Văn bản | Không có | **Tự động tạo VBĐi** trong `quan_ly_van_ban` khi lưu hợp đồng |
| Đơn hàng → Giao hàng → Hóa đơn | Không có | Chuỗi tự động, mỗi bước cập nhật trạng thái |

---

## 4. Module Văn bản (`quan_ly_van_ban`)

### 4.1 Model & dữ liệu

| Model | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| `van_ban_den` | Lưu trữ đơn giản | **5 trạng thái**, độ khẩn/độ mật, hạn xử lý, cron quá hạn, **email phân công** |
| `van_ban_di` | Tạo và lưu | Luồng duyệt, ký số, tự động tạo từ CRM, **email thông báo** |
| `loai_van_ban` | Không có | Danh mục loại, mã loại |
| `luong_duyet` + `buoc_duyet` | Không có | **Phê duyệt đa cấp** theo cấu hình, lịch sử từng bước |
| `chu_ky_dien_tu` | Không có | Upload file ký + **hash SHA256**, audit trail |
| `so_cong_van` | Không có | Sổ theo dõi VB đến/đi theo năm, mở/khóa sổ |
| `phieu_luan_chuyen` | Không có | Luân chuyển VB qua nhiều bộ phận, ghi nhận từng bước |
| `luu_tru_van_ban` | Không có | Lưu trữ vật lý (tủ/kệ/ngăn), thời hạn, thu hồi, đề xuất hủy |
| `chatbot_service` | Không có | **Chatbot AI Gemini 2.5 Flash** — tra cứu, hỏi đáp nghiệp vụ |
| `mau_van_ban` | Không có | Mẫu văn bản Jinja2, sinh VB từ mẫu |
| `lich_su_phien_ban` | Không có | Quản lý phiên bản tài liệu, diff |
| `email_log` | Không có | Nhật ký email tự động toàn hệ thống |

### 4.2 Frontend (JS/OWL)

| Tính năng | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Chatbot UI | Không có | **OWL Widget** — dialog chat floating, lịch sử hội thoại |
| Dashboard | Không có | **Custom OWL Dashboard** — số liệu thời gian thực, Chart.js |
| Upload chữ ký | Không có | Wizard upload với preview + xác nhận hash |

---

## 5. Tính năng bảo mật

| Tiêu chí | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Phân quyền model | Mặc định Odoo | **ACL chi tiết** cho từng model (ir.model.access.csv) |
| Chữ ký điện tử | Không có | Hash SHA256 cho file ký, audit trail |
| API key | Hardcode | Đọc từ **biến môi trường** `.env` (`GEMINI_API_KEY`, `GMAIL_APP_PASSWORD`) |
| Email password | Không có | App Password Gmail thay vì mật khẩu thật |

---

## 6. Hiệu năng & vận hành

| Tiêu chí | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Computed fields | Hầu hết tính realtime | `store=True` cho các field tính toán phức tạp (tong_thu_nhap, so_ngay) |
| Cron jobs | Không có | Cron tự động: hết hạn HĐ, quá hạn VBĐ |
| Sequences | Mã thủ công | `ir.sequence` tự sinh mã có prefix (NP/, CH/, VBD/...) |
| Docker | Không có | Docker Compose — PostgreSQL không phụ thuộc hệ thống cục bộ |
| Logging | Không có | Email log tập trung, tracking=True trên các field quan trọng |

---

## 7. So sánh luồng nghiệp vụ end-to-end

### Luồng Nhân sự

```
CŨ:  Tạo NV → Lưu (chỉ lưu thông tin)

MỚI: Tạo NV → Gán Phòng ban/Chức vụ
         → Tạo HĐLĐ (Draft → Hiệu lực, cron tự hết hạn)
         → Xin nghỉ phép (Nháp → Chờ duyệt → Duyệt + EMAIL)
         → Bảng lương (BHXH/BHYT/thuế TNCN 7 bậc → Chi trả + EMAIL)
         → KPI (5 tiêu chí → tự xếp loại)
         → Dashboard tổng hợp
```

### Luồng CRM bán hàng

```
CŨ:  Tạo KH → Lưu hợp đồng (thủ công)

MỚI: Tạo KH → Tạo Cơ hội → Pipeline 6 giai đoạn
         → Báo giá (chi tiết SP/DV) → KH đồng ý
         → Hợp đồng → Ký điện tử
         → Đơn hàng → Xác nhận (EMAIL KH) → Giao hàng
         → Hóa đơn → Thanh toán (EMAIL KH) → Công nợ
         → Lead scoring → Marketing → Khảo sát CSAT
         → VBĐi tự sinh trong module Văn bản (liên module)
```

### Luồng Văn bản

```
CŨ:  Tạo VB → Lưu (không có workflow)

MỚI: VBĐến: Nhận → Phân công (EMAIL) → Xử lý → Đã xử lý
                 (cron tự chuyển "Quá hạn" nếu trễ)
         → Luân chuyển đa bộ phận → Lưu trữ vật lý

     VBĐi: Soạn thảo → Luồng duyệt đa cấp → Ký điện tử (hash PKI)
               → Phát hành (EMAIL KH) → Lưu sổ công văn

     Chatbot: Hỏi đáp nghiệp vụ (Gemini AI) → Lịch sử chat
```

---

## 8. Thống kê kỹ thuật

| Chỉ số | Phiên bản cũ | Phiên bản mới |
|---|---|---|
| Số model tùy chỉnh | ~5 model | **51 model** (15 + 19 + 22 - phần dùng chung) |
| Số view XML | ~10 file | **57 file view XML** (17 + 25 + 25 - menu) |
| JS/OWL frontend | Không có | **6 file JS**, 3 file CSS, 4 file XML template |
| Email workflow | 0 sự kiện | **7 sự kiện tự động gửi email** |
| AI integration | Không có | Gemini 2.5 Flash REST API |
| Cron jobs | 0 | **2+ cron jobs**: hết hạn HĐ, quá hạn VBĐ |
| Sequences tự sinh | 0 | **6+ sequence**: NV, NP, BL, CH, VBD, VBDi |
| Docker service | Không có | PostgreSQL 10-alpine, port 5431 |
