# 📊 SO SÁNH PHIÊN BẢN: CŨ ↔ MỚI

> **Dự án**: ERP Quản lý Nhân sự – Khách hàng – Văn bản  
> **Nền tảng**: Odoo 15.0 · Python 3.10 · PostgreSQL  
> **Ngày cập nhật**: 22/03/2026

---

## 1. Tổng quan thay đổi

| Tiêu chí | Phiên bản cũ (v1.0) | Phiên bản mới (v2.0) | Thay đổi |
|----------|---------------------|---------------------|----------|
| **Tổng số model** | ~30 model | ~56 model | **+26 model mới** |
| **Tổng số file Python** | ~35 files | ~56 files | **+21 files** |
| **Tổng số XML views** | ~40 files | ~66 files | **+26 files** |
| **Module phụ thuộc** | `base`, `web`, `mail` | + `email_service`, `res_config_settings` | **+2 service** |
| **AI/LLM** | GPT-4o mini + Gemini (SDK) | Gemini 2.5 Flash (REST API) | **Đổi engine** |
| **Email** | Hardcode Gmail trong code | Dịch vụ tập trung + .env + UI Settings | **Chuẩn hóa** |
| **Báo cáo nâng cao** | Dashboard, Kanban, Graph cơ bản | + Calendar, Pivot, Graph nâng cao | **+3 loại view** |
| **Bảo mật** | Mật khẩu Gmail hardcode trong source | Đọc từ .env / ir.config_parameter | **Sửa lỗ hổng** |

---

## 2. So sánh chi tiết theo Module

### 2.1 Module `nhan_su` (HRM — Quản lý nhân sự)

#### Models

| Model | v1.0 (Cũ) | v2.0 (Mới) | Ghi chú |
|-------|-----------|-----------|---------|
| `nhan_vien` | ✅ ~15 trường cơ bản | ✅ **50+ trường** (CCCD, địa chỉ, trình độ, hôn nhân, ngân hàng, MST...) | Mở rộng lớn |
| `don_vi` | ✅ Có | ✅ Giữ nguyên | — |
| `chuc_vu` | ✅ Có | ✅ Giữ nguyên | — |
| `lich_su_cong_tac` | ✅ Có | ✅ Giữ nguyên | — |
| `chung_chi_bang_cap` | ✅ Có | ✅ Giữ nguyên | — |
| `hop_dong_lao_dong` | ❌ Không có | ✅ **MỚI**: 4 loại HĐ, lương+phụ cấp, workflow 5 TT, cron tự động | **+1 model** |
| `nghi_phep` + `so_nghi_phep` | ❌ Không có | ✅ **MỚI**: 6 loại phép, workflow duyệt, cân đối phép năm, **email thông báo** | **+2 model** |
| `bang_luong` | ❌ Không có | ✅ **MỚI**: BHXH/BHYT/BHTN, thuế TNCN 7 bậc, giảm trừ gia cảnh, **email chi trả** | **+1 model** |
| `danh_gia_kpi` | ❌ Không có | ✅ **MỚI**: 5 tiêu chí (1–5), tự phân loại, kỳ tháng/quý/năm | **+1 model** |
| `dao_tao` | ❌ Không có | ✅ **MỚI**: 4 hình thức, chi phí, danh sách NV tham gia | **+1 model** |
| `email_service` | ❌ Không có | ✅ **MỚI**: Dịch vụ email Gmail tập trung (AbstractModel) | **+1 service** |
| `res_config_settings` | ❌ Không có | ✅ **MỚI**: Cấu hình Gmail từ giao diện Odoo Settings | **+1 model** |

#### Views

| View | v1.0 | v2.0 | Ghi chú |
|------|------|------|---------|
| Form nhân viên | Đơn giản, ít tab | Avatar + header, 2 cột, 6 tab notebook, smart buttons | **Thiết kế lại** |
| Smart buttons | ❌ | ✅ 3 nút: Hợp đồng, Nghỉ phép, KPI | **Mới** |
| Calendar (nghỉ phép) | ❌ | ✅ Lịch nghỉ phép theo màu loại nghỉ | **Mới** |
| Calendar (đào tạo) | ❌ | ✅ Lịch đào tạo theo chương trình | **Mới** |
| Pivot (bảng lương) | ❌ | ✅ Phân tích lương theo đơn vị × tháng | **Mới** |
| Pivot (KPI) | ❌ | ✅ Phân tích KPI theo đơn vị × kỳ | **Mới** |
| Graph (lương) | ❌ | ✅ Biểu đồ cột thu nhập/thực lĩnh | **Mới** |
| Graph (KPI) | ❌ | ✅ Biểu đồ cột điểm trung bình | **Mới** |
| Settings email | ❌ | ✅ Giao diện cấu hình Gmail trong Cài đặt | **Mới** |
| Dashboard | ✅ Có | ✅ Giữ nguyên | — |

#### Workflow & Automation

| Tính năng | v1.0 | v2.0 |
|-----------|------|------|
| Sequence tự sinh mã | ❌ | ✅ HDLD-XXXX, NP-XXXX, BL-XXXX, KPI-XXXX, DT-XXXX |
| Cron job HĐLĐ hết hạn | ❌ | ✅ Tự động cập nhật trạng thái hàng ngày |
| Email duyệt nghỉ phép | ❌ | ✅ Gửi email tự động khi duyệt/từ chối |
| Email chi trả lương | ❌ | ✅ Gửi email chi tiết lương cho nhân viên |
| Sync res.partner | ❌ | ✅ Đồng bộ nhân viên ↔ res.partner |

---

### 2.2 Module `quan_ly_khach_hang` (CRM — Khách hàng & Bán hàng)

#### Models

| Model | v1.0 (Cũ) | v2.0 (Mới) | Ghi chú |
|-------|-----------|-----------|---------|
| `khach_hang` | ✅ Có | ✅ Giữ nguyên + sync partner | — |
| `co_hoi_ban_hang` | ✅ Pipeline 6 giai đoạn | ✅ Giữ nguyên + **email thắng/thua** | Thêm email |
| `bao_gia` | ✅ Có | ✅ Giữ nguyên | — |
| `hop_dong` | ✅ Có | ✅ Giữ nguyên | — |
| `don_hang` | ✅ Có | ✅ Giữ nguyên + **email xác nhận/hoàn thành** | Thêm email |
| `giao_hang` | ✅ Có | ✅ Giữ nguyên | — |
| `hoa_don` | ✅ Có | ✅ Giữ nguyên | — |
| `thanh_toan` | ✅ Có | ✅ Giữ nguyên | — |
| `cong_no_khach_hang` | ✅ Có | ✅ Giữ nguyên | — |
| `loyalty_program` | ✅ Có | ✅ Giữ nguyên | — |
| `khieu_nai_phan_hoi` | ✅ Có | ✅ Giữ nguyên | — |
| `tuong_tac_khach_hang` | ✅ Có | ✅ Giữ nguyên | — |
| `khao_sat_hai_long` | ❌ Không có | ✅ **MỚI**: CSAT (5 tiêu chí) / NPS (0–10) / CES | **+1 model** |
| `chien_dich_marketing` | ❌ Không có | ✅ **MỚI**: 7 loại chiến dịch, lọc KH tự động, KPI: ROI, tỷ lệ phản hồi | **+1 model** |
| `cham_diem_lead` | ❌ Không có | ✅ **MỚI**: Scoring 0–100 (5 yếu tố), Hot/Warm/Cold/Frozen, cron job | **+1 model** |

#### Views

| View | v1.0 | v2.0 | Ghi chú |
|------|------|------|---------|
| Graph đơn hàng (bar) | ❌ | ✅ Doanh thu theo trạng thái | **Mới** |
| Graph đơn hàng (line) | ❌ | ✅ Xu hướng đơn hàng theo tháng | **Mới** |
| Graph cơ hội (bar) | ❌ | ✅ Giá trị theo giai đoạn pipeline | **Mới** |
| Graph thanh toán (pie) | ❌ | ✅ Thống kê theo hình thức thanh toán | **Mới** |
| Pivot đơn hàng | ❌ | ✅ KH × trạng thái × giá trị | **Mới** |
| Pivot cơ hội | ❌ | ✅ NV phụ trách × giai đoạn × giá trị | **Mới** |
| Pivot tương tác | ❌ | ✅ Loại tương tác × nhân viên | **Mới** |
| Dashboard | ✅ Có | ✅ Giữ nguyên | — |
| Kanban cơ hội | ✅ Có | ✅ Giữ nguyên | — |

#### Workflow & Automation

| Tính năng | v1.0 | v2.0 |
|-----------|------|------|
| Email xác nhận đơn hàng | ❌ | ✅ Gửi cho KH khi đơn được xác nhận |
| Email hoàn thành đơn hàng | ✅ Có (mail.mail) | ✅ Giữ nguyên + thêm email từ service |
| Email thắng/thua cơ hội | ❌ | ✅ Gửi cho NV phụ trách |
| Cron scoring lead | ✅ Có | ✅ Giữ nguyên |
| Auto-create đơn hàng khi thắng | ✅ Có | ✅ Giữ nguyên |
| Tự động tạo VB từ cơ hội | ✅ Có | ✅ Giữ nguyên |

---

### 2.3 Module `quan_ly_van_ban` (QLVB — Quản lý văn bản)

#### Models

| Model | v1.0 (Cũ) | v2.0 (Mới) | Ghi chú |
|-------|-----------|-----------|---------|
| `van_ban_den` | ✅ Có | ✅ + **email phân công người xử lý** | Thêm email |
| `van_ban_di` | ✅ Có | ✅ **Sửa**: bỏ hardcode Gmail, dùng email service | **Fix bảo mật** |
| `loai_van_ban` | ✅ Có | ✅ Giữ nguyên | — |
| `luong_duyet` + `buoc_duyet` + `lich_su_duyet` | ✅ Có | ✅ Giữ nguyên | — |
| `chu_ky_dien_tu` | ✅ Có | ✅ Giữ nguyên | — |
| `mau_van_ban` | ✅ Có | ✅ Giữ nguyên | — |
| `lich_su_phien_ban` | ✅ Có | ✅ Giữ nguyên | — |
| `tai_lieu` | ✅ Có | ✅ Giữ nguyên | — |
| `chatbot_service` | ✅ GPT-4o mini + Gemini (SDK) | ✅ **Đổi**: chỉ Gemini 2.5 Flash (REST API), bỏ OpenAI | **Refactor lớn** |
| `so_cong_van` | ❌ Không có | ✅ **MỚI**: Sổ đến/đi theo năm + đơn vị, mở/khóa | **+1 model** |
| `phieu_luan_chuyen` + `chi_tiet` | ❌ Không có | ✅ **MỚI**: Luân chuyển VB qua bộ phận, lộ trình từng bước | **+2 model** |
| `luu_tru_van_ban` | ❌ Không có | ✅ **MỚI**: Lưu trữ vật lý, thời hạn, thu hồi, đề xuất hủy, cron cảnh báo | **+1 model** |
| `email_log` | ✅ Có | ✅ Giữ nguyên | — |

#### Views

| View | v1.0 | v2.0 | Ghi chú |
|------|------|------|---------|
| Calendar VB đến | ❌ | ✅ Theo ngày đến, màu theo độ khẩn | **Mới** |
| Calendar luân chuyển | ❌ | ✅ Theo ngày tạo phiếu | **Mới** |
| Graph VB đến (bar) | ❌ | ✅ Thống kê theo trạng thái | **Mới** |
| Graph VB đến (pie) | ❌ | ✅ Phân bổ theo độ khẩn | **Mới** |
| Graph VB đi (bar) | ❌ | ✅ Thống kê theo trạng thái | **Mới** |
| Pivot VB đến | ❌ | ✅ Loại VB × trạng thái | **Mới** |
| Pivot VB đi | ❌ | ✅ Loại VB × trạng thái | **Mới** |
| Dashboard | ✅ Có | ✅ Giữ nguyên | — |

#### Chatbot AI — Thay đổi lớn

| Tiêu chí | v1.0 | v2.0 |
|----------|------|------|
| **AI Provider** | OpenAI (GPT-4o mini) + Google Gemini | **Chỉ Google Gemini** |
| **Model AI** | gpt-4o-mini / gemini-pro | **gemini-2.5-flash** |
| **Cách gọi API** | OpenAI SDK + Google Generative AI SDK | **REST API thuần** (urllib.request) |
| **Dependency** | `openai`, `google-generativeai` | **Không cần SDK** (chỉ urllib) |
| **API endpoint** | Qua SDK | `generativelanguage.googleapis.com/v1beta/models/` |
| **Dropdown model** | 2 lựa chọn (GPT + Gemini) | 1 lựa chọn: Gemini 2.5 Flash |
| **Error handling** | Cơ bản | Xử lý 429/400/403/404 chi tiết |

---

## 3. Sửa lỗi bảo mật

| Vấn đề | v1.0 | v2.0 |
|--------|------|------|
| **Mật khẩu Gmail hardcode** | `sender_password = "xcnq ndxs iqxb tjws"` nằm trực tiếp trong `van_ban_di.py` | ✅ Đọc từ `.env` hoặc Odoo Settings. File `.env` được `.gitignore` |
| **API Key lộ trong code** | Có thể lộ qua git history | ✅ Tất cả key trong `.env` (gitignored) |
| **Gửi email phân tán** | Mỗi model tự xử lý SMTP | ✅ Dịch vụ tập trung `email.notification.service` |

---

## 4. Email thông báo — Tính năng mới hoàn toàn

| Sự kiện | Module | Email gửi cho | v1.0 | v2.0 |
|---------|--------|---------------|------|------|
| Duyệt nghỉ phép | HRM | Nhân viên | ❌ | ✅ |
| Từ chối nghỉ phép | HRM | Nhân viên | ❌ | ✅ |
| Chi trả lương | HRM | Nhân viên (chi tiết lương) | ❌ | ✅ |
| Xác nhận đơn hàng | CRM | Khách hàng | ❌ | ✅ |
| Hoàn thành đơn hàng | CRM | Khách hàng | ✅ (mail.mail) | ✅ (+ email service) |
| Cơ hội Thắng/Thua | CRM | NV phụ trách | ❌ | ✅ |
| Phân công VB đến | QLVB | Người xử lý | ❌ | ✅ |
| Phê duyệt VB đi | QLVB | Khách hàng | ✅ (hardcode Gmail) | ✅ (email service) |

---

## 5. Báo cáo nâng cao — Tính năng mới

| Loại view | Module | Nội dung | v1.0 | v2.0 |
|-----------|--------|----------|------|------|
| **Calendar** | HRM | Lịch nghỉ phép | ❌ | ✅ |
| **Calendar** | HRM | Lịch đào tạo | ❌ | ✅ |
| **Calendar** | QLVB | Lịch VB đến | ❌ | ✅ |
| **Calendar** | QLVB | Lịch luân chuyển | ❌ | ✅ |
| **Pivot** | HRM | Phân tích lương (đơn vị × tháng) | ❌ | ✅ |
| **Pivot** | HRM | Phân tích KPI (đơn vị × kỳ) | ❌ | ✅ |
| **Pivot** | CRM | Đơn hàng (KH × TT × giá trị) | ❌ | ✅ |
| **Pivot** | CRM | Pipeline (NV × giai đoạn × giá trị) | ❌ | ✅ |
| **Pivot** | CRM | Tương tác (loại × NV) | ❌ | ✅ |
| **Pivot** | QLVB | VB đến/đi (loại × trạng thái) | ❌ | ✅ |
| **Graph** | HRM | Biểu đồ lương, KPI | ❌ | ✅ |
| **Graph** | CRM | Đơn hàng (bar+line), cơ hội (bar), thanh toán (pie) | ❌ | ✅ |
| **Graph** | QLVB | VB đến (bar+pie), VB đi (bar) | ❌ | ✅ |

---

## 6. Thống kê tổng hợp

| Hạng mục | Cũ (v1.0) | Mới (v2.0) | Thêm mới |
|----------|-----------|-----------|----------|
| Model HRM | 7 | 14 | **+7** |
| Model CRM | 16 | 19 | **+3** |
| Model QLVB | 18 | 22 | **+4** |
| **Tổng model** | **~41** | **~55** | **+14** |
| View XML tổng | ~40 | ~66 | **+26** |
| Email tự động | 1 (hardcode) | 8 (dịch vụ tập trung) | **+7** |
| Calendar view | 0 | 4 | **+4** |
| Pivot view | 0 | 8 | **+8** |
| Graph view nâng cao | 0 | 9 | **+9** |
| AI Engine | 2 (OpenAI + Gemini SDK) | 1 (Gemini REST API) | Tinh gọn |
| Bảo mật .env | ❌ | ✅ | Fix |

---

## 7. Công nghệ mới sử dụng

| Công nghệ | Mục đích | v1.0 | v2.0 |
|-----------|----------|------|------|
| Gemini 2.5 Flash REST API | Chatbot AI | ❌ (dùng SDK) | ✅ urllib.request thuần |
| Gmail SMTP Service | Email thông báo tập trung | ❌ (hardcode) | ✅ AbstractModel |
| .env configuration | Bảo mật API keys | ❌ | ✅ |
| Odoo Settings UI | Cấu hình email từ giao diện | ❌ | ✅ res.config.settings |
| Calendar View | Lịch trực quan | ❌ | ✅ 4 calendar views |
| Pivot View | Phân tích đa chiều | ❌ | ✅ 8 pivot views |
