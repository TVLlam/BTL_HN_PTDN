<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    ERP: HỆ THỐNG QUẢN LÝ NHÂN SỰ – KHÁCH HÀNG – VĂN BẢN
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of IT](https://img.shields.io/badge/Faculty%20of%20IT-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)
[![Odoo 15](https://img.shields.io/badge/Odoo-15.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 📖 1. Giới thiệu

**ERP: Hệ thống quản lý Nhân sự – Khách hàng – Văn bản** là hệ thống quản trị doanh nghiệp được xây dựng trên nền tảng **Odoo 15.0 (mã nguồn mở)**, phục vụ học phần *Thực tập doanh nghiệp* — Khoa CNTT, Trường Đại học Đại Nam.

Hệ thống gồm **3 module chính** tích hợp chặt chẽ:

| Module | Mô tả |
|--------|-------|
| **`nhan_su`** (HRM) | Quản lý nhân viên, phòng ban, hợp đồng LĐ, nghỉ phép, bảng lương, KPI, đào tạo |
| **`quan_ly_khach_hang`** (CRM) | Pipeline bán hàng end-to-end: khách hàng → cơ hội → báo giá → hợp đồng → đơn hàng → giao hàng → hóa đơn → thanh toán |
| **`quan_ly_van_ban`** (QLVB) | Văn bản đến/đi, phê duyệt đa cấp, ký số, OCR, chatbot AI, sổ công văn, luân chuyển, lưu trữ |

### Điểm nổi bật

- **Tích hợp liên module**: HRM cung cấp master data nhân sự cho CRM và QLVB; CRM liên kết tự động với QLVB qua hợp đồng/cơ hội
- **AI & Automation**: Chatbot Gemini 2.5 Flash, OCR trích xuất văn bản, tóm tắt nội dung tự động
- **Email thông báo Gmail**: Tự động gửi email khi duyệt nghỉ phép, chi trả lương, xác nhận đơn hàng, phân công văn bản
- **Báo cáo nâng cao**: Dashboard, Calendar, Pivot, Graph cho mọi module
- **Chữ ký điện tử**: Ký số trực tiếp trên văn bản, xác thực hash

---

## 👥 2. Thành viên thực hiện

| STT | Mã SV | Họ và tên | Lớp | Nhóm |
|-----|-------|-----------|------|------|
| 1 | 1771020412 | Trần Văn Lâm | CNTT 17-07 | Nhóm 4 |
| 2 | 1771020158 | Dương Ngọc Đông | CNTT 17-07 | Nhóm 4 |
| 3 | 11771020519 | Nguyễn Thị Thanh Nhã | CNTT 17-07 | Nhóm 4 |

---

## 🔧 3. Công nghệ sử dụng

<div align="center">

| Thành phần | Công nghệ |
|------------|-----------|
| **Nền tảng** | Odoo 15.0 Community |
| **Backend** | Python 3.10 |
| **Frontend** | JavaScript (OWL Framework), XML Views |
| **Database** | PostgreSQL 14 (Docker) |
| **AI/LLM** | Google Gemini 2.5 Flash (REST API) |
| **Email** | Gmail SMTP (App Password) |
| **OS** | Ubuntu / WSL2 |

[![Odoo](https://img.shields.io/badge/Odoo_15-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python_3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Gemini](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

</div>

---

## 🏗️ 4. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────┐
│                    Client (Browser)                      │
│                 http://localhost:8069                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Odoo Server                            │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ nhan_su  │  │quan_ly_khach │  │ quan_ly_van_ban   │  │
│  │  (HRM)   │◄─┤  _hang (CRM) │◄─┤    (Document)     │  │
│  │          │  │              │  │                   │  │
│  │• Nhân viên│  │• Khách hàng  │  │• Văn bản đến/đi   │  │
│  │• Hợp đồng│  │• Cơ hội      │  │• Phê duyệt/Ký số  │  │
│  │• Nghỉ phép│  │• Đơn hàng    │  │• OCR / Chatbot AI │  │
│  │• Bảng lương│ │• Thanh toán  │  │• Sổ công văn      │  │
│  │• KPI     │  │• Marketing   │  │• Luân chuyển      │  │
│  │• Đào tạo │  │• Lead Score  │  │• Lưu trữ          │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
│                                                          │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Email Notification Service (Gmail SMTP)            │ │
│  │  Gemini AI REST API  │  Chữ ký điện tử (PKI)      │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            PostgreSQL (Docker - port 5431)                │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 5. Chi tiết chức năng theo module

### 5.1 Module `nhan_su` — Quản lý nhân sự (HRM)

| Model | Chức năng |
|-------|-----------|
| `nhan_vien` | Hồ sơ nhân viên (50+ trường): thông tin cá nhân, CCCD, trình độ, ngân hàng, trạng thái làm việc |
| `don_vi` | Cơ cấu phòng ban / đơn vị tổ chức |
| `chuc_vu` | Danh mục chức vụ, cấp độ |
| `hop_dong_lao_dong` | Vòng đời HĐLĐ: 4 loại, lương + phụ cấp, workflow 5 trạng thái, cron tự động |
| `nghi_phep` + `so_nghi_phep` | 6 loại phép, workflow duyệt, cân đối phép năm + **email thông báo** |
| `bang_luong` | Tính lương: BHXH/BHYT/BHTN, thuế TNCN 7 bậc, giảm trừ gia cảnh + **email khi chi trả** |
| `danh_gia_kpi` | 5 tiêu chí (1–5), tự phân loại xuất sắc→yếu, kỳ tháng/quý/năm |
| `dao_tao` | 4 hình thức đào tạo, chi phí, danh sách NV tham gia |
| `lich_su_cong_tac` | Lịch sử điều động, thuyên chuyển |
| `chung_chi_bang_cap` | Quản lý chứng chỉ, bằng cấp nhân viên |
| `email_service` | Dịch vụ gửi email Gmail tập trung cho toàn hệ thống |

**Views**: Form, Tree, Kanban, Graph, Dashboard, Calendar (nghỉ phép, đào tạo), Pivot (lương, KPI)

### 5.2 Module `quan_ly_khach_hang` — CRM / Bán hàng

| Model | Chức năng |
|-------|-----------|
| `khach_hang` | Hồ sơ KH cá nhân/doanh nghiệp, phân tầng (Đồng→Kim cương) |
| `co_hoi_ban_hang` | Pipeline 6 giai đoạn (Mới→Thắng/Thua) + **email thắng/thua** |
| `bao_gia` | Báo giá chi tiết, workflow KH đồng ý/từ chối |
| `hop_dong` | Hợp đồng bán hàng, chữ ký điện tử |
| `don_hang` + `don_hang_chi_tiet` | Đơn hàng, sản phẩm/dịch vụ + **email xác nhận/hoàn thành** |
| `giao_hang` | Phiếu giao hàng, xác nhận vận chuyển |
| `hoa_don` | Hóa đơn bán hàng |
| `thanh_toan` | Thanh toán nhiều hình thức |
| `cong_no_khach_hang` | Bảng điều khiển công nợ |
| `khao_sat_hai_long` | CSAT / NPS / CES — đo hài lòng KH |
| `chien_dich_marketing` | 7 loại chiến dịch, lọc KH tự động, KPI (ROI, tỷ lệ phản hồi) |
| `cham_diem_lead` | Scoring 0–100, xếp hạng Hot/Warm/Cold/Frozen |
| `loyalty_program` | Chương trình thân thiết, tích điểm |
| `khieu_nai_phan_hoi` | Khiếu nại, SLA, mức ưu tiên |

**Views**: Form, Tree, Kanban, Graph (đơn hàng, cơ hội, thanh toán), Pivot (đơn hàng, pipeline, tương tác), Dashboard, Calendar

### 5.3 Module `quan_ly_van_ban` — Quản lý văn bản

| Model | Chức năng |
|-------|-----------|
| `van_ban_den` | Tiếp nhận, phân công, xử lý VB đến + **email phân công** |
| `van_ban_di` | Soạn thảo, phê duyệt, ký số, gửi VB đi + **email thông báo KH** |
| `loai_van_ban` | Danh mục loại văn bản |
| `luong_duyet` + `buoc_duyet` + `lich_su_duyet` | Phê duyệt đa cấp theo cấu hình |
| `chu_ky_dien_tu` | Ký số PKI, xác thực hash, lưu audit trail |
| `so_cong_van` | Sổ theo dõi VB đến/đi theo năm, mở/khóa sổ |
| `phieu_luan_chuyen` | Luân chuyển VB qua bộ phận, chi tiết từng bước |
| `luu_tru_van_ban` | Lưu trữ vật lý (tủ/kệ/ngăn), thời hạn, thu hồi, đề xuất hủy |
| `chatbot_service` | Chatbot AI Gemini 2.5 Flash — tra cứu dữ liệu, hỏi đáp |
| `mau_van_ban` | Quản lý mẫu văn bản |
| `lich_su_phien_ban` | Quản lý phiên bản tài liệu |
| `email_log` | Nhật ký email tự động |
| `tai_lieu` | Lưu trữ tài liệu đính kèm |

**Views**: Form, Tree, Kanban, Calendar (VB đến, luân chuyển), Graph (VB đến/đi), Pivot (VB đến/đi), Dashboard

---

## 🔗 6. Tích hợp liên module

```
nhan_su (HRM)          quan_ly_khach_hang (CRM)        quan_ly_van_ban (QLVB)
    │                          │                              │
    │ ← depends ──────────────┘                              │
    │ ← depends ─────────────────────────────────────────────┘
    │                          │ ← depends ───────────────────┘
    │                          │
    ├── nhan_vien ──────► nhan_vien_phu_trach_id       nguoi_xu_ly_id
    ├── don_vi ─────────► (phòng ban KH)               (phòng ban VB)
    ├── email_service ──► gửi email đơn hàng           gửi email VB
    │                          │
    │                     co_hoi_ban_hang ────────► van_ban_den (auto-create)
    │                     hop_dong ───────────────► van_ban_di (auto-create)
    │                     don_hang ───────────────► giao_hang → hoa_don → thanh_toan
```

- **HRM → CRM**: Nhân viên phụ trách khách hàng, cơ hội, đơn hàng
- **HRM → QLVB**: Người xử lý văn bản, người duyệt, người ký
- **CRM → QLVB**: Tự động tạo văn bản từ hợp đồng/cơ hội bán hàng
- **Email Service**: Dịch vụ tập trung tại `nhan_su`, dùng chung bởi cả 3 module

---

## ⚙️ 7. Cài đặt và chạy

### 7.1 Yêu cầu

- Ubuntu 20.04+ / WSL2
- Python 3.10
- Docker & Docker Compose
- Gmail + App Password (cho tính năng email)
- Gemini API Key (cho chatbot AI)

### 7.2 Cài đặt nhanh

```bash
# 1. Clone project
git clone <repo-url> TTDN-16-01-N4
cd TTDN-16-01-N4

# 2. Cài thư viện hệ thống
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev \
  libssl-dev python3.10-distutils python3.10-dev build-essential libffi-dev \
  zlib1g-dev python3.10-venv libpq-dev

# 3. Tạo môi trường ảo
python3.10 -m venv ./venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install cryptography==41.0.7 pyOpenSSL==23.3.0 urllib3==1.26.18

# 4. Khởi động PostgreSQL (Docker)
sudo docker-compose up -d

# 5. Cấu hình odoo.conf
cp odoo.conf.template odoo.conf
# Sửa nếu cần (port, db_name...)

# 6. Cấu hình .env (email + AI)
cat > .env << 'EOF'
GEMINI_API_KEY=your-gemini-api-key
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
EOF

# 7. Cài đặt module lần đầu
python3 odoo-bin.py -c odoo.conf -d tranvanlam -i nhan_su,quan_ly_khach_hang,quan_ly_van_ban --stop-after-init

# 8. Chạy server
python3 odoo-bin.py -c odoo.conf -d tranvanlam
```

Truy cập: **http://localhost:8069** — Đăng nhập: `admin` / `admin`

### 7.3 Cập nhật module

```bash
# Dừng server (Ctrl+C), sau đó:
python3 odoo-bin.py -c odoo.conf -d tranvanlam -u nhan_su,quan_ly_khach_hang,quan_ly_van_ban --stop-after-init
python3 odoo-bin.py -c odoo.conf -d tranvanlam
```

---

## 📁 8. Cấu trúc thư mục

```
TTDN-16-01-N4/
├── odoo-bin.py              # Entry point
├── odoo.conf                # Cấu hình Odoo
├── .env                     # API keys + Gmail (gitignored)
├── docker-compose.yml       # PostgreSQL container
├── requirements.txt         # Python dependencies
│
├── addons/
│   ├── nhan_su/                     # Module Nhân sự (HRM)
│   │   ├── models/                  # 15 model files
│   │   │   ├── nhan_vien.py         # Hồ sơ nhân viên
│   │   │   ├── hop_dong_lao_dong.py # Hợp đồng lao động
│   │   │   ├── nghi_phep.py         # Nghỉ phép + email
│   │   │   ├── bang_luong.py        # Bảng lương + email
│   │   │   ├── danh_gia_kpi.py      # Đánh giá KPI
│   │   │   ├── dao_tao.py           # Đào tạo
│   │   │   ├── email_service.py     # Dịch vụ email tập trung
│   │   │   └── ...
│   │   ├── views/                   # 16 XML view files
│   │   │   ├── advanced_views.xml   # Calendar, Pivot, Graph
│   │   │   ├── res_config_settings_views.xml  # Cấu hình email
│   │   │   └── ...
│   │   └── security/
│   │
│   ├── quan_ly_khach_hang/          # Module CRM
│   │   ├── models/                  # 19 model files
│   │   │   ├── khach_hang.py        # Hồ sơ khách hàng
│   │   │   ├── co_hoi_ban_hang.py   # Pipeline + email
│   │   │   ├── don_hang.py          # Đơn hàng + email
│   │   │   ├── cham_diem_lead.py    # Lead scoring
│   │   │   ├── khao_sat_hai_long.py # CSAT/NPS
│   │   │   └── ...
│   │   ├── views/                   # 25 XML view files
│   │   │   ├── advanced_views.xml   # Graph, Pivot
│   │   │   └── ...
│   │   └── security/
│   │
│   └── quan_ly_van_ban/             # Module QLVB
│       ├── models/                  # 22 model files
│       │   ├── van_ban_den.py       # VB đến + email
│       │   ├── van_ban_di.py        # VB đi + email
│       │   ├── chatbot_service.py   # Gemini AI chatbot
│       │   ├── chu_ky_dien_tu.py    # Chữ ký điện tử
│       │   ├── phieu_luan_chuyen.py # Phiếu luân chuyển
│       │   └── ...
│       ├── views/                   # 25 XML view files
│       │   ├── advanced_views.xml   # Calendar, Graph, Pivot
│       │   └── ...
│       ├── static/src/js/           # Chatbot UI (JS)
│       └── security/
│
├── odoo/                    # Odoo core framework (không sửa)
├── docs/                    # Tài liệu, logo, hình ảnh
└── setup/                   # Scripts cài đặt
```

---

## 🎨 9. Giao diện hệ thống

### Dashboard tổng quan
<p align="center">
  <img src="https://github.com/user-attachments/assets/4feafa52-32d1-481d-a300-e7ed13a1ec32" width="900"/>
</p>

### Quản lý nhân sự
<p align="center">
  <img src="https://github.com/user-attachments/assets/64ebdfdd-92e6-4d34-a508-9ac472356676" width="900"/>
</p>

### Dashboard khách hàng
<p align="center">
  <img src="https://github.com/user-attachments/assets/e2962e2b-012a-41d3-b724-2def46e292cd" width="900"/>
</p>

### Quản lý văn bản
<p align="center">
  <img src="https://github.com/user-attachments/assets/ed3a6559-a815-4430-9d3b-a9fd0a642560" width="900"/>
</p>

### Chatbot AI Gemini
<p align="center">
  <img src="https://github.com/user-attachments/assets/a39f4bed-adae-49b3-8f70-e74efb92d64b" width="900"/>
</p>

---

## 🔥 10. Demo

🎥 **Video demo**: https://drive.google.com/file/d/1XpkW_k6fBDpILEwmaxLWcl24tdXTLVJb/view?usp=sharing

---

## 📚 11. Tài liệu liên quan

| File | Mô tả |
|------|-------|
| [SO_SANH_CU_MOI.md](SO_SANH_CU_MOI.md) | So sánh chi tiết giữa phiên bản cũ và mới |
| [HUONG_DAN_TEST.md](HUONG_DAN_TEST.md) | Hướng dẫn test toàn bộ dự án từ đầu đến cuối |
| [upgrade-plan.md](upgrade-plan.md) | Kế hoạch nâng cấp chi tiết |

---

## 📎 12. Nguồn tham khảo

* **Repository CRM tham khảo**: [TTDN-15-05-N2](https://github.com/yukiharadev/TTDN-15-05-N2)
* **Repository QLVB tham khảo**: [TTDN-15-04-N2](https://github.com/ngocanhit201/TTDN-15-04-N2)
* **Nền tảng học phần**: [Business-Internship (FIT-DNU)](https://github.com/FIT-DNU/Business-Internship)

---

## 🖼️ Poster

<p align="center">
  <img width="709" height="1024" alt="Poster" src="https://github.com/user-attachments/assets/e1477dff-d1db-4011-9553-f9cccee1dec6"/>
</p>

---

## 📝 License

© 2024–2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.
