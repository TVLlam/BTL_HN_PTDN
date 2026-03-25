# KẾ HOẠCH NÂNG CẤP — ERP: Quản lý Nhân sự – Khách hàng – Văn bản

> **Phiên bản hiện tại**: 1.0 (hoàn thành)  
> **Nền tảng**: Odoo 15.0 Community · Python 3.10 · PostgreSQL 10 (Docker)  
> **Nhóm**: CNTT17-07 — Nhóm 4  
> **Cập nhật**: 25/03/2026

---

## MỤC LỤC

1. [Trạng thái hiện tại (v1.0)](#1-trạng-thái-hiện-tại-v10)
2. [Kiến trúc hiện tại](#2-kiến-trúc-hiện-tại)
3. [Lộ trình nâng cấp](#3-lộ-trình-nâng-cấp)
4. [Phase 2 — Tự động hóa quy trình](#4-phase-2--tự-động-hóa-quy-trình)
5. [Phase 3 — AI & Tích hợp ngoài](#5-phase-3--ai--tích-hợp-ngoài)
6. [Phase 4 — Hạ tầng & CI/CD](#6-phase-4--hạ-tầng--cicd)
7. [Bảng ưu tiên nâng cấp](#7-bảng-ưu-tiên-nâng-cấp)

---

## 1. Trạng thái hiện tại (v1.0)

### Đã hoàn thành ✅

#### Module `nhan_su` — Nhân sự (HRM)
- [x] Quản lý nhân viên (50+ trường: CCCD, trình độ, ngân hàng, ảnh, trạng thái)
- [x] Phòng ban, chức vụ phân cấp
- [x] Hợp đồng lao động: 4 loại, workflow 3 trạng thái, cron tự hết hạn
- [x] Nghỉ phép: 7 loại, workflow 5 trạng thái, email thông báo khi duyệt
- [x] Bảng lương: BHXH/BHYT/BHTN tự tính, thuế TNCN 7 bậc, email khi chi trả
- [x] Đánh giá KPI: 5 tiêu chí, tự xếp loại 5 mức, kỳ tháng/quý/năm
- [x] Đào tạo: 4 hình thức, Calendar view
- [x] Lịch sử công tác, điều động
- [x] Chứng chỉ, bằng cấp có file đính kèm
- [x] Email service Gmail SMTP tập trung
- [x] Dashboard OWL + Chart.js
- [x] Views: Form, Tree, Kanban, Graph, Calendar, Pivot, Dashboard

#### Module `quan_ly_khach_hang` — CRM / Bán hàng
- [x] Khách hàng cá nhân/doanh nghiệp, phân tầng (Đồng→Kim cương)
- [x] Pipeline cơ hội 6 giai đoạn, email thắng/thua
- [x] Báo giá chi tiết, KH đồng ý/từ chối
- [x] Hợp đồng bán hàng với chữ ký điện tử (upload + hash)
- [x] Đơn hàng → Giao hàng → Hóa đơn → Thanh toán (chuỗi hoàn chỉnh)
- [x] Email xác nhận/hoàn thành đơn hàng
- [x] Dashboard công nợ khách hàng
- [x] Lead scoring 0–100 (Hot/Warm/Cold/Frozen)
- [x] Chiến dịch marketing (7 loại)
- [x] Khảo sát hài lòng (CSAT/NPS/CES)
- [x] Chương trình loyalty tích điểm
- [x] Khiếu nại/phản hồi với SLA
- [x] Tự động tạo VBĐi khi lưu hợp đồng CRM
- [x] Views: Form, Tree, Kanban, Graph, Pivot, Calendar, Dashboard

#### Module `quan_ly_van_ban` — Quản lý văn bản (QLVB)
- [x] Văn bản đến: 5 trạng thái, độ khẩn/mật, cron quá hạn, email phân công
- [x] Văn bản đi: luồng duyệt, ký số, email phát hành
- [x] Phê duyệt đa cấp (luồng duyệt cấu hình linh hoạt)
- [x] Chữ ký điện tử: upload file + hash SHA256 + audit trail
- [x] Sổ công văn đến/đi theo năm, mở/khóa sổ
- [x] Phiếu luân chuyển văn bản qua bộ phận
- [x] Lưu trữ vật lý (tủ/kệ/ngăn), thời hạn, đề xuất hủy
- [x] Chatbot AI Gemini 2.5 Flash (tra cứu nghiệp vụ)
- [x] Mẫu văn bản Jinja2
- [x] Lịch sử phiên bản tài liệu
- [x] Email log toàn hệ thống
- [x] Views: Form, Tree, Kanban, Graph, Pivot, Calendar, Dashboard

---

## 2. Kiến trúc hiện tại

```
CNTT17-07-NHOM4/
├── odoo-bin.py              # Entry point chính
├── odoo.conf                # Cấu hình server (port 8069, db 5431)
├── .env                     # GEMINI_API_KEY, GMAIL_EMAIL, GMAIL_APP_PASSWORD
├── docker-compose.yml       # PostgreSQL 10-alpine, port 5431
├── requirements.txt         # Python dependencies
│
└── addons/
    ├── nhan_su/             # v1.0 — HRM (15 models, 16 views, OWL dashboard)
    │   ├── models/          # nhan_vien, hop_dong_lao_dong, nghi_phep,
    │   │                    # bang_luong, danh_gia_kpi, dao_tao, email_service...
    │   ├── views/           # 16 XML files + CSS/JS/XML templates
    │   └── security/
    │
    ├── quan_ly_khach_hang/  # v1.0 — CRM (19 models, 25 views, OWL dashboard)
    │   ├── models/          # khach_hang, co_hoi_ban_hang, bao_gia, hop_dong,
    │   │                    # don_hang, giao_hang, hoa_don, thanh_toan...
    │   ├── views/           # 25 XML files + CSS/JS/XML templates
    │   └── security/
    │
    └── quan_ly_van_ban/     # v1.0 — QLVB (22 models, 25 views, Chatbot OWL)
        ├── models/          # van_ban_den, van_ban_di, luong_duyet, chu_ky,
        │                    # chatbot_service, so_cong_van, luu_tru...
        ├── views/           # 25 XML files + CSS/JS/XML templates
        ├── static/src/js/   # chatbot_dialog.js, qlvb_dashboard.js
        └── security/
```

**Phụ thuộc module**:
```
base, web, mail
    └── nhan_su (v1.0)
            └── quan_ly_khach_hang (v1.0)
                        └── quan_ly_van_ban (v1.0)
```

---

## 3. Lộ trình nâng cấp

```
v1.0 (Hiện tại)     v2.0 (Phase 2)        v3.0 (Phase 3)        v4.0 (Phase 4)
─────────────────   ──────────────────    ──────────────────    ──────────────────
3 module hoàn       Tự động hóa sâu       AI mở rộng            CI/CD & Scale
chỉnh, email,       hơn, report PDF,      OCR thông minh,       Production deploy
chatbot cơ bản      API webhook           PKI thật, Telegram     Docker Swarm
```

---

## 4. Phase 2 — Tự động hóa quy trình

**Mục tiêu**: Giảm thao tác thủ công, tăng tự động hóa nghiệp vụ.

### 4.1 Module `nhan_su` — Nâng cấp

| Hạng mục | Mô tả | Ưu tiên |
|---|---|---|
| **Bảng lương tự động** | Cron tính lương tự động theo tháng, không cần tạo thủ công | Cao |
| **Onboarding checklist** | Khi tạo NV mới → tự sinh danh sách việc cần làm (cấp badge, email welcome) | Trung bình |
| **Cảnh báo hết hạn HĐ** | Cron gửi email 30/15/7 ngày trước khi HĐ hết hạn | Cao |
| **Phê duyệt nghỉ phép đa cấp** | Nghỉ > 3 ngày → qua 2 lớp duyệt (trưởng phòng + HR) | Trung bình |
| **Nhân viên portal** | NV tự xem hồ sơ, phiếu lương, lịch nghỉ phép qua Odoo portal | Thấp |
| **Export báo cáo PDF** | In phiếu lương, hợp đồng, đánh giá KPI ra PDF | Cao |
| **Biểu mẫu** | Tích hợp HTML form chuẩn cho HĐLĐ, quyết định, quy trình| Trung bình |

### 4.2 Module `quan_ly_khach_hang` — Nâng cấp

| Hạng mục | Mô tả | Ưu tiên |
|---|---|---|
| **SLA cảnh báo cơ hội** | Cron cảnh báo cơ hội không có hoạt động > N ngày | Cao |
| **Tự động tạo đơn hàng từ hợp đồng** | Khi HĐ ký xong → tự tạo đơn hàng đầu tiên | Trung bình |
| **Báo cáo doanh thu PDF** | Xuất báo cáo doanh thu theo KH, NV, tháng ra PDF | Cao |
| **Nhắc công nợ tự động** | Cron gửi email nhắc KH còn nợ > N ngày quá hạn | Cao |
| **Portal khách hàng** | KH tự xem đơn hàng, hóa đơn, lịch sử mua qua portal | Thấp |
| **Webhook tích hợp ngoài** | REST API cho phép hệ thống ngoài push cơ hội/đơn hàng | Trung bình |
| **Giá theo từng KH** | Bảng giá riêng theo phân tầng KH | Trung bình |

### 4.3 Module `quan_ly_van_ban` — Nâng cấp

| Hạng mục | Mô tả | Ưu tiên |
|---|---|---|
| **Báo cáo VB PDF** | Xuất báo cáo tổng hợp VB đến/đi theo tháng/loại ra PDF | Cao |
| **Nhắc hạn xử lý tự động** | Cron gửi email nhắc VBĐ sắp đến hạn (T-2 ngày) | Cao |
| **Duyệt qua email** | Người duyệt click link trong email để duyệt, không cần đăng nhập | Trung bình |
| **Sinh số VB tự động theo sổ** | Số VB tự sinh theo sổ (VBD-2026-001, VBDi-2026-001) | Cao |
| **Tìm kiếm fulltext** | PostgreSQL FTS cho nội dung/tóm tắt văn bản | Trung bình |
| **Phân quyền record-level** | Record rules: NV chỉ xem VB phòng mình | Trung bình |

---

## 5. Phase 3 — AI & Tích hợp ngoài

**Mục tiêu**: Ứng dụng công nghệ mới, mở rộng kết nối với dịch vụ ngoài.

### 5.1 Nâng cấp AI

| Hạng mục | Mô tả |
|---|---|
| **OCR thông minh** | Tích hợp Google Vision API hoặc Tesseract để OCR PDF/ảnh VB đến → tự điền trường |
| **Tóm tắt hợp đồng AI** | Gửi nội dung HĐ lên Gemini → trả về tóm tắt điều khoản chính |
| **Gợi ý trả lời email** | Gemini đề xuất nội dung reply email cho VB đến |
| **Phân tích KPI AI** | AI phân tích xu hướng KPI, đề xuất cải thiện |
| **Chatbot nâng cao** | Function calling để chatbot thực hiện hành động (tạo nghỉ phép qua chat) |

### 5.2 Tích hợp dịch vụ ngoài

| Dịch vụ | Mô tả |
|---|---|
| **Ký số PKI thật** | Tích hợp VNPT-CA / FPT-CA / Viettel-CA thay cho ký số nội bộ |
| **Google Calendar** | Đồng bộ lịch nghỉ phép, đào tạo, deadline VB ra Google Calendar |
| **Telegram / Zalo** | Gửi thông báo quan trọng (duyệt lương, VB quá hạn) qua Telegram Bot / Zalo OA |
| **PowerBI / Metabase** | Kết nối database ra dashboard phân tích BI |
| **REST API public** | Expose API để mobile app hoặc hệ thống ngoài truy vấn dữ liệu |

---

## 6. Phase 4 — Hạ tầng & CI/CD

**Mục tiêu**: Triển khai production, pipeline tự động, bảo đảm ổn định.

### 6.1 CI/CD

```yaml
# Gợi ý .github/workflows/ci.yml
stages:
  - lint:       pylint, flake8 cho toàn bộ addons custom
  - test:       pytest-odoo với database test riêng
  - build:      Docker image
  - deploy:     Deploy lên VPS / cloud (nếu có)
```

| Hạng mục | Công cụ |
|---|---|
| Linting | `pylint` + Odoo plugin + `flake8` |
| Unit test | `pytest-odoo` hoặc `odoo.tests.common.TransactionCase` |
| Docker build | `Dockerfile` + `docker-compose.prod.yml` |
| Secrets | GitHub Secrets cho `GEMINI_API_KEY`, `GMAIL_APP_PASSWORD` |

### 6.2 Production deployment

| Hạng mục | Mô tả |
|---|---|
| **Nginx reverse proxy** | HTTPS (Let's Encrypt), gzip, cache static |
| **PostgreSQL production** | PostgreSQL 14+, backup hàng ngày, WAL archiving |
| **Odoo workers** | Multi-process workers (`workers = 4`) cho production load |
| **Redis session** | Lưu session vào Redis thay vì filesystem |
| **Monitoring** | Uptime monitoring (UptimeRobot), log Grafana/Loki |
| **Backup** | pg_dump tự động về S3/Rclone hàng ngày |

### 6.3 Bảo mật production

| Hạng mục | Mô tả |
|---|---|
| `.env` không commit | `.gitignore` đã có, cần xác nhận CI không leak |
| HTTPS bắt buộc | `proxy_mode = True` trong `odoo.conf` |
| Mật khẩu admin | Đổi `admin`/`admin` thành mật khẩu mạnh ngay khi deploy |
| Rate limiting | Nginx limit_req cho login endpoint |
| Audit log | Bật `ir.logging` cho các thao tác quan trọng |

---

## 7. Bảng ưu tiên nâng cấp

| STT | Hạng mục | Module | Phase | Ưu tiên | Độ phức tạp |
|---|---|---|---|---|---|
| 1 | Cảnh báo hết hạn hợp đồng LĐ (email) | nhan_su | 2 | 🔴 Cao | Thấp |
| 2 | Nhắc hạn xử lý VB tự động | quan_ly_van_ban | 2 | 🔴 Cao | Thấp |
| 3 | Export phiếu lương PDF | nhan_su | 2 | 🔴 Cao | Trung bình |
| 4 | Nhắc công nợ KH tự động | quan_ly_khach_hang | 2 | 🔴 Cao | Thấp |
| 5 | Sinh số VB tự động theo sổ | quan_ly_van_ban | 2 | 🔴 Cao | Thấp |
| 6 | Báo cáo VB PDF | quan_ly_van_ban | 2 | 🔴 Cao | Trung bình |
| 7 | SLA cảnh báo cơ hội không hoạt động | quan_ly_khach_hang | 2 | 🟡 TB | Thấp |
| 8 | Phê duyệt nghỉ phép đa cấp | nhan_su | 2 | 🟡 TB | Trung bình |
| 9 | Record rules phân quyền VB | quan_ly_van_ban | 2 | 🟡 TB | Trung bình |
| 10 | OCR văn bản đến | quan_ly_van_ban | 3 | 🟡 TB | Cao |
| 11 | Tóm tắt hợp đồng AI | quan_ly_khach_hang | 3 | 🟡 TB | Trung bình |
| 12 | Ký số PKI thật (VNPT-CA) | quan_ly_van_ban | 3 | 🟢 Thấp | Cao |
| 13 | Google Calendar sync | nhan_su | 3 | 🟢 Thấp | Trung bình |
| 14 | Telegram Bot thông báo | All | 3 | 🟢 Thấp | Trung bình |
| 15 | CI/CD pipeline | DevOps | 4 | 🟡 TB | Cao |
| 16 | Production Docker + Nginx | DevOps | 4 | 🔴 Cao | Cao |

---

> **Nguyên tắc nâng cấp**: Không sửa trực tiếp Odoo core. Mọi thay đổi thực hiện qua custom addon trong `addons/`. Trước khi nâng cấp phiên bản Odoo (15→16→17), kiểm tra tương thích toàn bộ 3 module custom.
