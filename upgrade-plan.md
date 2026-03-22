# Kế hoạch nâng cấp ERP (HRM / CRM / Document)

> **Phiên bản:** 2.0 — Cập nhật ngày 22/03/2026  
> **Nền tảng:** Odoo 15.0 · Python 3.10 · PostgreSQL (Docker)

---

## MỤC LỤC
1. [Mục tiêu và phạm vi](#1-mục-tiêu-và-phạm-vi)
2. [Kiến trúc đích dự kiến](#2-kiến-trúc-đích-dự-kiến)
3. [Roadmap & Lộ trình nâng cấp](#3-roadmap-tổng-quan)
4. [Công việc chi tiết theo module](#4-công-việc-chi-tiết-theo-module-có-mở-rộng)
5. [Tích hợp liên module](#5-tích-hợp-liên-module-erp)
6. [BẢNG SO SÁNH: Code cũ ↔ Code nâng cấp](#6-bảng-so-sánh-code-cũ--code-nâng-cấp)
7. [CHI TIẾT CÁC TÍNH NĂNG NÂNG CẤP ĐÃ TRIỂN KHAI](#7-chi-tiết-các-tính-năng-nâng-cấp-đã-triển-khai)
8. [Bảo mật, quyền, tuân thủ](#8-bảo-mật-quyền-tuân-thủ)
9. [Testing và QA](#9-testing-và-qa)
10. [Triển khai](#10-triển-khai)
11. [KPI thành công](#11-kpi-thành-công)

---

## 1. Mục tiêu và phạm vi
- Tách rõ 3 module: HRM (nhân sự), CRM (khách hàng/bán hàng), Document (quản lý văn bản) thành các addon riêng để dễ bảo trì và mở rộng.
- Dùng ERP (Odoo) làm lớp tích hợp: chia sẻ master data, quy trình duyệt, chu kỳ nghiệp vụ, báo cáo tập trung.
- Nâng cấp có hệ thống so với dự án cũ: bổ sung workflow duyệt/ ký số, OCR, dashboard KPI, tự động hóa sự kiện, bảo mật và CI/CD.
- Không sửa trực tiếp core Odoo; kế thừa và mở rộng bằng custom addon trong `addons/`.

## 2. Kiến trúc đích dự kiến
- **HRM addon**: mở rộng từ `hr`, `hr_contract`, `hr_attendance`, `hr_skills`; làm nguồn nhân sự cho CRM/Document.
- **CRM addon**: mở rộng từ `crm`, `sale`, `sale_management`, liên kết `account` (hóa đơn) và `stock` (giao/nhập hàng nếu có).
- **Document addon**: mở rộng `documents`, `mail`, `sign` (hoặc PKI ngoài), thêm OCR qua API, workflow duyệt đa cấp.
- **Layer tích hợp (ERP)**:
  - Chia sẻ `res.partner` (khách hàng), `hr.employee` (nhân sự) làm master data liên module.
  - Event/cron đồng bộ CRM ↔ Document (tạo hồ sơ văn bản từ hợp đồng, cơ hội; tự động đính kèm hóa đơn).
  - ACL/record rule đồng bộ cho 3 module: Admin, HR, Sales, Legal/Document, User.

## 3. Roadmap tổng quan
- **Phase 0: Kiến trúc & nền tảng**
  - Kiểm kê addon hiện có; tách custom khỏi core; định danh thư mục `addons/custom_hrm`, `custom_crm`, `custom_document`.
  - Thiết lập CI lint/test (pre-commit, pylint, odoo linter) và pipeline build.

## 3.1 Lộ trình 3 mức nâng cấp (thực hiện tuần tự)
- **Mức 1 – Tích hợp hệ thống (System Integration)**
  - Đảm bảo dữ liệu thống nhất: HRM cung cấp dữ liệu gốc đồng bộ sang CRM và Document (nhân sự, lương, phòng ban, người phụ trách).
  - Ghép nối cơ sở dữ liệu, bỏ nhập liệu trùng lặp; chuẩn hóa master data `res.partner`, `hr.employee`.
  - Kết quả: 3 module dùng chung DB, tránh sai lệch dữ liệu, luồng cơ bản thông suốt.
- **Mức 2 – Tự động hóa quy trình (Process Automation)**
  - Bắn sự kiện (event-driven): khi báo giá được chấp nhận → tự động tạo hợp đồng/văn bản; khi hợp đồng ký → tự động cập nhật hóa đơn, task follow-up.
  - Giảm thao tác thủ công: server action/cron cho nhắc hạn xử lý văn bản, nhắc nợ, SLA pipeline CRM.
  - Kết quả: người dùng nhập ít hơn, hệ thống tự chạy luồng tiếp nối.
- **Mức 3 – Ứng dụng công nghệ mới (AI & External API)**
  - Tích hợp AI/LLM: trợ lý hỏi đáp quy trình, tóm tắt hợp đồng/văn bản, OCR thông minh cho hóa đơn/CV.
  - External API: kết nối ký số PKI, đồng bộ lịch (Google Calendar), nhắc việc/notify qua Telegram/Zalo/email.
  - Kết quả: trải nghiệm nâng cấp rõ rệt, tự động thông minh và mở rộng kết nối.

## 3.2 Đột phá so với dự án cũ
- Bổ sung OCR và ký số tích hợp sâu vào Document; trước đây không có hoặc rời rạc.
- Chuỗi phê duyệt đa cấp dựa trên sơ đồ tổ chức HRM, áp vào CRM và Document.
- Event-driven giữa CRM ↔ Document (tự sinh văn bản/hợp đồng) thay cho thao tác tay.
- Dashboard KPI liên module (HR/CRM/Document) và cảnh báo SLA thời gian thực.

## 4. Công việc chi tiết theo module (có mở rộng)
### 4.1 HRM
- Model: mở rộng `hr.employee` (hồ sơ, chứng chỉ, tài liệu kèm), `hr.department` (cơ cấu), job position, ma trận phê duyệt theo chức danh.
- Workflow: on/off-boarding; phê duyệt nghỉ phép, công tác, chi phí (tận dụng `hr_holidays`, `hr_expense`).
- Lịch sử công tác, đánh giá (mở rộng `hr_appraisal` nếu cần), chấm công nâng cao (geo/time fence nếu bổ sung).
- API/Tích hợp: webhook/REST cấp danh bạ nhân sự cho CRM/Document; đồng bộ user → employee → partner (phục vụ ký số).

### 4.2 CRM / Khách hàng
- Pipeline: cơ hội với KPI chuyển đổi, SLA theo stage, cảnh báo trễ hạn; playbook nhiệm vụ tự động.
- Báo giá/hợp đồng: mở rộng `sale.order` và `account.move` gắn với Document; hợp đồng sinh văn bản để duyệt/ ký.
- Quản lý tương tác: email, cuộc gọi, meeting (`calendar`), log hoạt động; chăm sóc sau bán và nhắc thu hồi công nợ.
- Chính sách giá/khuyến mại: tận dụng `coupon`, loyalty nếu cần; cấu hình điều kiện động.
- Công nợ/thu hồi: bảng điều khiển công nợ; trigger nhắc nợ đa kênh.

### 4.3 Document / Văn bản
- Model: văn bản đến, văn bản đi, hợp đồng; trường: số hiệu, loại, đơn vị ban hành/nhận, bảo mật, hạn xử lý, liên kết partner/hợp đồng.
- Workflow duyệt: nhiều cấp (cấu hình từ org chart HRM); trạng thái: nháp → chờ duyệt → đã duyệt → ký → phát hành/lưu trữ.
- Liên kết CRM: tạo văn bản từ báo giá/hợp đồng; tự động đính kèm hóa đơn/PO; cập nhật trạng thái khi ký thành công.
- Tích hợp ký số: Odoo Sign hoặc API PKI (VNPT/FPT/Viettel); lưu audit trail và file đã ký.
- OCR: tích hợp API (Google Vision, Tesseract service) để trích xuất trường từ PDF/ảnh, map vào metadata tìm kiếm.
- Phiên bản và lưu trữ: `documents` với versioning, tagging, indexing; quota và dọn dẹp.

## 5. Tích hợp liên module (ERP)
- HRM cung cấp danh bạ nhân sự, phòng ban, vai trò để dựng chuỗi phê duyệt/ ký cho CRM và Document.
- CRM dùng `res.partner`; Document liên kết văn bản với partner và hợp đồng; tự động cập nhật trạng thái văn bản khi hợp đồng ký hoặc hóa đơn thanh toán.
- Sự kiện tự động: server action/cron tạo văn bản khi báo giá được chấp nhận; tạo task theo dõi khi văn bản sắp tới hạn; nhắc nợ khi hóa đơn quá hạn.
- Báo cáo tập trung: dashboard KPI HR (nhân sự, phê duyệt), CRM (pipeline, doanh thu), Document (số lượng đến/đi, SLA) trên một menu chung.

## 5.1 Đánh giá hiện trạng & triển khai
- **Audit code (hiện trạng):** Kiểm thử mã nguồn cũ, lập danh sách lỗi tồn, điểm nợ kỹ thuật, chức năng thiếu so với yêu cầu 3 mức.
- **Gap analysis:** Xác định phần kế thừa được (model, view, security) và phần cần phát triển mới để đáp ứng tích hợp + automation + AI/API.
- **Implementation (tích hợp & đồng bộ):** Ghép nối code, xử lý xung đột dữ liệu, chuẩn hóa quy trình nghiệp vụ giữa HRM – CRM – Document; thêm migration script nếu đổi model.

---

## 6. BẢNG SO SÁNH: Code cũ ↔ Code nâng cấp

### 6.1 Module `nhan_su` (Quản lý nhân sự — HRM)

| Tiêu chí | Code cũ | Code nâng cấp |
|----------|---------|----------------|
| **Model chính** | `nhan_vien` (mã, họ tên, ngày sinh, SĐT, email, ảnh) | `nhan_vien` mở rộng +20 trường: giới tính, CCCD, địa chỉ, trình độ, hôn nhân, dân tộc, tôn giáo, ngân hàng, MST, ngày vào làm, trạng thái LV |
| **Model phụ** | `don_vi`, `chuc_vu`, `lich_su_cong_tac`, `chung_chi_bang_cap` | Giữ nguyên + thêm **5 model mới** |
| **Hợp đồng LĐ** | ❌ Không có | ✅ `hop_dong_lao_dong`: 4 loại (thử việc/xác định/không TH/thời vụ), lương + phụ cấp (ăn/đi lại/ĐT/khác), workflow 5 trạng thái, cron tự động cập nhật hết hạn |
| **Nghỉ phép** | ❌ Không có | ✅ `nghi_phep` + `so_nghi_phep`: 6 loại phép (năm/ốm/thai sản/cưới/tang/việc riêng), approval workflow, tự tính ngày, cân đối phép năm |
| **Bảng lương** | ❌ Không có | ✅ `bang_luong`: tính lương theo ngày công, BHXH 8%/BHYT 1.5%/BHTN 1%, thuế TNCN 7 bậc lũy tiến, giảm trừ bản thân 11tr + phụ thuộc 4.4tr, workflow nháp→xác nhận→đã chi |
| **Đánh giá KPI** | ❌ Không có | ✅ `danh_gia_kpi`: 5 tiêu chí (hoàn thành CV/chất lượng/sáng tạo/làm việc nhóm/kỷ luật), thang 1–5, tự phân loại (xuất sắc→yếu), kỳ tháng/quý/năm |
| **Đào tạo** | ❌ Không có | ✅ `dao_tao`: 4 hình thức (nội bộ/bên ngoài/online/hội thảo), Many2many NV, chi phí, số giờ, kết quả đánh giá |
| **Smart button** | ❌ Không có | ✅ 3 smart button trên form nhân viên: Hợp đồng LĐ, Nghỉ phép, Đánh giá KPI |
| **Form view** | Đơn giản, ít tab | Thiết kế lại: avatar + header, 2 cột (cá nhân + công việc), 6 tab notebook |
| **Menu** | Dashboard, NV, Danh mục | Dashboard, NV, HĐLĐ, Nghỉ phép (đơn + số phép), Bảng lương, KPI, Đào tạo, Lịch sử CT, Danh mục |
| **Tích hợp ERP** | ❌ | ✅ `partner_id` sync với `res.partner` |
| **Sequence** | ❌ | ✅ Auto-sequence cho mỗi model mới (HDLD-XXXX, NP-XXXX, BL-XXXX, KPI-XXXX, DT-XXXX) |

### 6.2 Module `quan_ly_khach_hang` (CRM / Khách hàng)

| Tiêu chí | Code cũ | Code nâng cấp |
|----------|---------|----------------|
| **Chức năng CRM** | Khách hàng, hợp đồng, báo giá, tài liệu | Giữ nguyên tất cả + thêm **3 tính năng mới** |
| **Pipeline bán hàng** | Cơ hội → Báo giá → Hợp đồng → Đơn hàng → Giao hàng → Hóa đơn → Thanh toán | Giữ nguyên toàn bộ pipeline |
| **Khảo sát hài lòng** | ❌ Không có | ✅ `khao_sat_hai_long`: 3 loại (CSAT/NPS/CES), 5 tiêu chí đánh giá (tổng thể/chất lượng/giao hàng/hỗ trợ/giá), NPS 0-10 phân nhóm Promoter/Passive/Detractor, workflow gửi→phản hồi→đóng |
| **Chiến dịch Marketing** | ❌ Không có | ✅ `chien_dich_marketing`: 7 loại (Email/SMS/sự kiện/khuyến mại/giới thiệu/content/khác), lọc KH tự động theo phân tầng & vòng đời, KPI: ngân sách, chi phí, ROI, tỷ lệ phản hồi |
| **Chấm điểm Lead** | ❌ Không có | ✅ `cham_diem_lead`: tự động tính điểm 0–100 dựa trên 5 yếu tố (tương tác 25đ + doanh thu 30đ + phản hồi KS 15đ + trung thành 15đ + cơ hội 15đ), xếp hạng Hot/Warm/Cold/Frozen, cron job tính lại định kỳ |
| **Loyalty program** | Có (chương trình thân thiết, điểm, ưu đãi) | Giữ nguyên |
| **Khiếu nại & Phản hồi** | Có (mã, loại, ưu tiên, SLA) | Giữ nguyên |
| **Công nợ** | Có (tổng nợ, nợ quá hạn, bảng điều khiển) | Giữ nguyên |

### 6.3 Module `quan_ly_van_ban` (Quản lý văn bản)

| Tiêu chí | Code cũ | Code nâng cấp |
|----------|---------|----------------|
| **Chức năng VB** | VB đến/đi, hợp đồng, báo giá, tài liệu, phê duyệt, ký số, mẫu VB, luồng duyệt | Giữ nguyên tất cả + thêm **3 tính năng mới** |
| **Sổ công văn** | ❌ Không có | ✅ `so_cong_van`: Sổ theo dõi văn bản đến/đi theo năm & đơn vị, mở/khóa sổ, thống kê số lượng, liên kết trực tiếp với VB đến/đi qua `so_cong_van_id` |
| **Phiếu luân chuyển** | ❌ Không có | ✅ `phieu_luan_chuyen` + `chi_tiet`: Theo dõi luân chuyển văn bản qua các bộ phận, lộ trình tuần tự (nhận→xử lý→chuyển tiếp), ý kiến chỉ đạo, hạn xử lý, tự động hoàn tất khi hết bước |
| **Lưu trữ & Thu hồi** | ❌ Không có | ✅ `luu_tru_van_ban`: Quản lý lưu trữ vật lý (vị trí tủ/kệ/ngăn), thời hạn (5/10/20 năm/vĩnh viễn), tự tính ngày hết hạn, workflow lưu trữ→đề xuất hủy→duyệt hủy, thu hồi & lưu lại, cron cảnh báo sắp hết hạn |
| **OCR / AI** | Có (trích xuất + tóm tắt) | Giữ nguyên |
| **Chữ ký điện tử** | Có (PKI, hash, xác thực) | Giữ nguyên |
| **Lịch sử phiên bản** | Có (diff visualization) | Giữ nguyên |
| **Chatbot AI** | Có (GPT-4o mini, Gemini) | Giữ nguyên |
| **Luồng duyệt** | Có (đa cấp, bước duyệt) | Giữ nguyên |

---

## 7. CHI TIẾT CÁC TÍNH NĂNG NÂNG CẤP ĐÃ TRIỂN KHAI

### 7.1 Module nhan_su — Tính năng mới

#### 7.1.1 Hợp đồng lao động (`hop_dong_lao_dong`)
- **File:** `models/hop_dong_lao_dong.py`, `views/hop_dong_lao_dong.xml`
- **Mô tả:** Quản lý toàn bộ vòng đời hợp đồng lao động
- **Loại HĐ:** Thử việc, Xác định thời hạn, Không xác định thời hạn, Thời vụ
- **Thông tin lương:** Lương cơ bản + 4 khoản phụ cấp (ăn, đi lại, điện thoại, khác) → tự tính tổng thu nhập
- **Workflow:** Mới → Hiệu lực → Sắp hết hạn → Hết hạn → Chấm dứt
- **Tự động:** Cron job kiểm tra hợp đồng sắp/đã hết hạn và cập nhật trạng thái
- **Sequence:** `HDLD-2026-0001`

#### 7.1.2 Nghỉ phép (`nghi_phep` + `so_nghi_phep`)
- **File:** `models/nghi_phep.py`, `views/nghi_phep.xml`
- **Mô tả:** Quản lý đơn xin nghỉ phép và cân đối phép năm
- **6 loại phép:** Phép năm, Ốm đau, Thai sản, Cưới, Tang, Việc riêng
- **Workflow duyệt:** Nháp → Chờ duyệt → Duyệt / Từ chối / Hủy
- **Tự tính ngày:** Dựa trên ngày bắt đầu – ngày kết thúc, kiểm tra ngày hợp lệ
- **Số ngày phép:** Theo dõi tổng phép, đã dùng, còn lại theo nhân viên × năm
- **Sequence:** `NP-2026-0001`

#### 7.1.3 Bảng lương (`bang_luong`)
- **File:** `models/bang_luong.py`, `views/bang_luong.xml`
- **Mô tả:** Tính lương hàng tháng theo chuẩn pháp luật Việt Nam
- **Công thức:**
  - Thu nhập = Lương cơ bản × (ngày công / 26) + Phụ cấp
  - BHXH 8%, BHYT 1.5%, BHTN 1% (trên lương cơ bản)
  - Thuế TNCN lũy tiến 7 bậc (5% → 35%)
  - Giảm trừ bản thân: 11,000,000 VNĐ/tháng
  - Giảm trừ phụ thuộc: 4,400,000 VNĐ/người/tháng
- **Tính năng:** Nút kéo lương từ HĐLĐ đang hiệu lực, form 3 tab (Thu nhập, Khấu trừ, Thực lĩnh)
- **Workflow:** Nháp → Xác nhận → Đã chi
- **Sequence:** `BL-2026-0001`

#### 7.1.4 Đánh giá KPI (`danh_gia_kpi`)
- **File:** `models/danh_gia_kpi.py`, `views/danh_gia_kpi.xml`
- **Mô tả:** Đánh giá hiệu suất nhân viên theo 5 tiêu chí
- **5 tiêu chí (thang 1–5):** Hoàn thành công việc, Chất lượng, Sáng tạo, Làm việc nhóm, Kỷ luật
- **Phân loại tự động:** Xuất sắc (≥4.5) / Tốt (≥3.5) / Khá (≥2.5) / Trung bình (≥1.5) / Yếu (<1.5)
- **Kỳ đánh giá:** Tháng, Quý, Năm
- **Nội dung bổ sung:** Tự đánh giá, đánh giá quản lý, mục tiêu kỳ tới
- **Sequence:** `KPI-2026-0001`

#### 7.1.5 Đào tạo (`dao_tao`)
- **File:** `models/dao_tao.py`, `views/dao_tao.xml`
- **Mô tả:** Quản lý chương trình đào tạo nhân viên
- **4 hình thức:** Nội bộ, Bên ngoài, Online, Hội thảo
- **Thông tin:** Tên CT, giảng viên, nhân viên tham gia (Many2many), chi phí, số giờ
- **Workflow:** Dự kiến → Đang diễn ra → Hoàn thành / Hủy
- **Sequence:** `DT-2026-0001`

#### 7.1.6 Nâng cấp form nhân viên
- **Smart buttons:** 3 nút (Hợp đồng LĐ, Nghỉ phép, Đánh giá KPI) với counter
- **Layout mới:** Avatar + oe_title, 2 cột thông tin, 6 tab notebook
- **Trường mới trên form:** Giới tính, CCCD, địa chỉ, trình độ, hôn nhân, dân tộc, tôn giáo, ngân hàng, MST, trạng thái làm việc (badge màu)

---

### 7.2 Module quan_ly_khach_hang — Tính năng mới

#### 7.2.1 Khảo sát hài lòng khách hàng (`khao_sat_hai_long`)
- **File:** `models/khao_sat_hai_long.py`, `views/khao_sat_hai_long.xml`
- **Mô tả:** Đo lường mức độ hài lòng khách hàng qua nhiều phương pháp
- **3 loại khảo sát:**
  - **CSAT:** Đánh giá tổng thể, chất lượng SP/DV, giao hàng, hỗ trợ, giá cả (thang 1–5)
  - **NPS:** Điểm 0–10, tự phân nhóm Promoter (9–10) / Passive (7–8) / Detractor (0–6)
  - **CES:** Mức độ dễ dàng sử dụng dịch vụ
- **Tính toán:** Điểm trung bình tự động, NPS group tự phân loại
- **Workflow:** Nháp → Đã gửi → Đã phản hồi → Đóng
- **Search/Group:** Theo loại khảo sát, trạng thái, nhóm NPS, khách hàng
- **Sequence:** `KS-2026-0001`

#### 7.2.2 Chiến dịch Marketing (`chien_dich_marketing`)
- **File:** `models/chien_dich_marketing.py`, `views/chien_dich_marketing.xml`
- **Mô tả:** Lập kế hoạch và đo lường hiệu quả chiến dịch marketing
- **7 loại chiến dịch:** Email, SMS, Sự kiện, Khuyến mại, Giới thiệu, Content, Khác
- **Phân khúc mục tiêu:**
  - Tất cả khách hàng
  - Theo phân tầng (Đồng/Bạc/Vàng/Kim cương)
  - Theo vòng đời (Hoạt động/Không hoạt động/Rời bỏ)
  - Tùy chọn thủ công
- **Nút lọc tự động:** Lọc khách hàng theo tiêu chí đã chọn, gán vào chiến dịch
- **KPI theo dõi:** Số KH mục tiêu, số phản hồi, tỷ lệ phản hồi (%), số cơ hội tạo, doanh thu, ROI (%)
- **Workflow:** Nháp → Lên kế hoạch → Đang chạy → Hoàn thành / Hủy
- **Sequence:** `MKT-2026-0001`

#### 7.2.3 Chấm điểm Lead tự động (`cham_diem_lead`)
- **File:** `models/cham_diem_lead.py`, `views/cham_diem_lead.xml`
- **Mô tả:** Chấm điểm khách hàng tiềm năng để ưu tiên chăm sóc
- **5 tiêu chí tính điểm (tổng max 100):**

| Tiêu chí | Max | Cách tính |
|----------|-----|-----------|
| Tương tác | 25 | Số lần tương tác trong 90 ngày × 5 |
| Doanh thu | 30 | Doanh thu 12 tháng: ≥1 tỷ=30, ≥500tr=25, ≥200tr=20, ≥50tr=15, >0=10 |
| Phản hồi KS | 15 | Điểm TB khảo sát gần nhất × 3 |
| Trung thành | 15 | Số HĐLĐ hiệu lực × 5 |
| Cơ hội mở | 15 | Số cơ hội đang mở × 5 |

- **Xếp hạng tự động:**
  - 🔥 **Hot** (≥70 điểm) — Ưu tiên chăm sóc ngay
  - 🟡 **Warm** (40–69) — Tiềm năng, cần nuôi dưỡng
  - 🔵 **Cold** (15–39) — Theo dõi dài hạn
  - ⬜ **Frozen** (<15) — Không hoạt động
- **Cron job:** Tự động tạo bản ghi cho KH mới và tính lại điểm toàn bộ
- **Ràng buộc:** Mỗi khách hàng chỉ có 1 bảng chấm điểm (SQL unique)

---

### 7.3 Module quan_ly_van_ban — Tính năng mới

#### 7.3.1 Sổ công văn (`so_cong_van`)
- **File:** `models/so_cong_van.py`, `views/so_cong_van.xml`
- **Mô tả:** Quản lý sổ theo dõi văn bản đến/đi theo năm và đơn vị
- **Tính năng:**
  - Sổ công văn đến / Sổ công văn đi (tách biệt)
  - Theo năm + đơn vị/phòng ban (unique constraint)
  - Người quản lý sổ
  - Tự đếm số lượng văn bản trong sổ
  - Workflow: Đang mở ↔ Đã khóa
- **Liên kết:** Thêm trường `so_cong_van_id` vào cả `van_ban_den` và `van_ban_di`
- **Sequence:** `SCV-2026-001`

#### 7.3.2 Phiếu luân chuyển văn bản (`phieu_luan_chuyen`)
- **File:** `models/phieu_luan_chuyen.py`, `views/phieu_luan_chuyen.xml`
- **Mô tả:** Theo dõi lộ trình luân chuyển văn bản qua các bộ phận
- **Tính năng:**
  - Liên kết với VB đến hoặc VB đi
  - Ý kiến chỉ đạo, hạn xử lý
  - **Lộ trình chi tiết** (inline editable tree): Thứ tự → Người nhận → Đơn vị → Trạng thái
  - Mỗi bước: Chờ nhận → Đã nhận → Đã xử lý → Chuyển tiếp (có nút hành động)
  - Tự động hoàn tất khi hết bước cuối
  - Workflow: Nháp → Đang luân chuyển → Hoàn tất / Thu hồi
- **Sequence:** `LC-2026-0001`

#### 7.3.3 Lưu trữ & Thu hồi văn bản (`luu_tru_van_ban`)
- **File:** `models/luu_tru_van_ban.py`, `views/luu_tru_van_ban.xml`
- **Mô tả:** Quản lý lưu trữ vật lý và vòng đời hủy văn bản
- **Tính năng:**
  - Vị trí lưu trữ vật lý (Tủ/Kệ/Ngăn/Hộp)
  - Thời hạn lưu trữ: 5, 10, 20 năm hoặc Vĩnh viễn
  - Tự tính ngày hết hạn lưu trữ
  - **Thu hồi:** Ghi lý do, người thu hồi, ngày thu hồi → có thể lưu trữ lại
  - **Hủy:** Đề xuất hủy → Duyệt hủy (ghi người duyệt, ngày hủy, lý do)
  - **Cron cảnh báo:** Tự động post message khi văn bản sắp hết hạn lưu trữ (30 ngày)
  - Workflow: Đang lưu trữ → Chờ hủy → Đã hủy | Thu hồi → Lưu trữ lại
- **Sequence:** `LT-2026-0001`

---

## 8. Bảo mật, quyền, tuân thủ
- Vai trò: Admin, HR Manager, Sales Manager, Document Manager, User xem; record rule theo phòng ban, owner, vai trò duyệt.
- Ẩn thông tin nhạy cảm (lương, định danh) chỉ HR thấy; mã hóa file lưu trữ nếu cần.
- Audit log: ghi nhận ký số, thay đổi trạng thái, tải file; nhật ký truy cập.
- Backup/DR: sao lưu DB và file định kỳ; kế hoạch khôi phục.

## 9. Testing và QA
- Unit test cho logic model; tour test UI cho luồng duyệt, ký số, tạo văn bản từ hợp đồng.
- Dữ liệu mẫu: script seed nhân sự, khách hàng, văn bản/hợp đồng demo.
- CI pipeline: lint (`pylint`, `black` nếu dùng), test Odoo (`--test-enable`), build addon.

## 10. Triển khai
- Môi trường: dev (hot reload), staging (dữ liệu mẫu), prod (backup, monitoring).
- Docker compose cập nhật: db, odoo, OCR service (nếu tự host), reverse proxy HTTPS.
- Hiệu năng: cấu hình workers, longpolling, tách file store ra object storage nếu tài liệu lớn.

## 11. Kế hoạch dữ liệu và di trú
- Mapping từ hệ thống cũ (nếu có) sang model mới; script ETL bằng `base_import` hoặc psycopg2.
- Chuẩn hóa đặt tên, số hiệu văn bản; constraint kiểm tra trùng/thiếu.

## 12. KPI thành công
- Giảm thời gian xử lý văn bản X%, tăng tỷ lệ chuyển đổi cơ hội Y%, SLA đúng hạn Z%.
- Ba module độc lập nhưng liên kết dữ liệu xuyên suốt; CI/CD ổn định; không lỗi nghiệp vụ chính trong test tự động.
