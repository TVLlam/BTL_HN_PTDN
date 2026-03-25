# -*- coding: utf-8 -*-
"""
Script thêm dữ liệu mẫu toàn diện cho 3 module:
  - nhan_su (Nhân sự)
  - quan_ly_khach_hang (CRM / Khách hàng)
  - quan_ly_van_ban (Văn bản)

Cách chạy (trong terminal, với Odoo đang chạy ở terminal khác):
  cd /home/tranvanlam/CNTT17-07-NHOM4
  source venv/bin/activate
  python3 odoo-bin.py shell -c odoo.conf -d tranvanlam < seed_data.py
"""

from datetime import date, timedelta

env = self.env  # noqa: F821  – 'self' được Odoo shell cung cấp

# Tắt mail gửi thực để không bị lỗi outgoing server
env = env(context=dict(env.context, mail_notrack=True, no_recompute=True))

print("=" * 60)
print("BẮT ĐẦU TẠO DỮ LIỆU MẪU")
print("=" * 60)

# ============================================================
# MODULE NHÂN SỰ
# ============================================================
print("\n>>> [1/3] MODULE NHÂN SỰ")

# --- 1. Đơn vị / Phòng ban ---
print("  Tạo phòng ban...")
phong_ban_data = [
    {"ma_don_vi": "BGD", "ten_don_vi": "Ban Giám đốc", "cap_do": 1},
    {"ma_don_vi": "PHKT", "ten_don_vi": "Phòng Hành chính - Kế toán", "cap_do": 2},
    {"ma_don_vi": "PHNS", "ten_don_vi": "Phòng Nhân sự", "cap_do": 2},
    {"ma_don_vi": "PHKD", "ten_don_vi": "Phòng Kinh doanh", "cap_do": 2},
    {"ma_don_vi": "PHKT2", "ten_don_vi": "Phòng Kỹ thuật - CNTT", "cap_do": 2},
]
phong_ban = {}
for d in phong_ban_data:
    existing = env["don_vi"].search([("ma_don_vi", "=", d["ma_don_vi"])], limit=1)
    if existing:
        phong_ban[d["ma_don_vi"]] = existing
    else:
        phong_ban[d["ma_don_vi"]] = env["don_vi"].create(d)
print(f"  -> {len(phong_ban)} phòng ban.")

# --- 2. Chức vụ ---
print("  Tạo chức vụ...")
chuc_vu_data = [
    {"ma_chuc_vu": "GD",   "ten_chuc_vu": "Giám đốc",              "cap_do": 1},
    {"ma_chuc_vu": "PGD",  "ten_chuc_vu": "Phó Giám đốc",          "cap_do": 2},
    {"ma_chuc_vu": "TP",   "ten_chuc_vu": "Trưởng phòng",          "cap_do": 3},
    {"ma_chuc_vu": "PP",   "ten_chuc_vu": "Phó phòng",             "cap_do": 4},
    {"ma_chuc_vu": "NV",   "ten_chuc_vu": "Nhân viên",             "cap_do": 5},
    {"ma_chuc_vu": "KTV",  "ten_chuc_vu": "Kỹ thuật viên",         "cap_do": 5},
    {"ma_chuc_vu": "NV_KD","ten_chuc_vu": "Nhân viên Kinh doanh",  "cap_do": 5},
]
chuc_vu = {}
for d in chuc_vu_data:
    existing = env["chuc_vu"].search([("ma_chuc_vu", "=", d["ma_chuc_vu"])], limit=1)
    if existing:
        chuc_vu[d["ma_chuc_vu"]] = existing
    else:
        chuc_vu[d["ma_chuc_vu"]] = env["chuc_vu"].create(d)
print(f"  -> {len(chuc_vu)} chức vụ.")

# --- 3. Nhân viên ---
print("  Tạo nhân viên...")
nhan_vien_data = [
    {
        "ma_dinh_danh": "NV001", "ho_ten_dem": "Nguyễn Văn", "ten": "An",
        "ngay_sinh": date(1980, 3, 15), "gioi_tinh": "nam",
        "email": "nguyenvanan@company.vn", "so_dien_thoai": "0901234567",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "da_ket_hon",
        "que_quan": "Hà Nội", "dia_chi_hien_tai": "123 Đường Láng, Đống Đa, Hà Nội",
        "luong_co_ban": 25000000, "ngay_vao_lam": date(2018, 1, 10),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "BGD", "_cv": "GD",
    },
    {
        "ma_dinh_danh": "NV002", "ho_ten_dem": "Trần Thị", "ten": "Bình",
        "ngay_sinh": date(1985, 7, 22), "gioi_tinh": "nu",
        "email": "tranthibinh@company.vn", "so_dien_thoai": "0912345678",
        "trinh_do_hoc_van": "thac_si", "tinh_trang_hon_nhan": "da_ket_hon",
        "que_quan": "Hải Phòng", "dia_chi_hien_tai": "456 Trần Phú, Hà Đông, Hà Nội",
        "luong_co_ban": 18000000, "ngay_vao_lam": date(2019, 3, 1),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHNS", "_cv": "TP",
    },
    {
        "ma_dinh_danh": "NV003", "ho_ten_dem": "Lê Minh", "ten": "Cường",
        "ngay_sinh": date(1990, 11, 5), "gioi_tinh": "nam",
        "email": "leminhcuong@company.vn", "so_dien_thoai": "0923456789",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "doc_than",
        "que_quan": "Đà Nẵng", "dia_chi_hien_tai": "789 Đinh Tiên Hoàng, Hai Bà Trưng, HN",
        "luong_co_ban": 15000000, "ngay_vao_lam": date(2020, 6, 15),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKD", "_cv": "NV_KD",
    },
    {
        "ma_dinh_danh": "NV004", "ho_ten_dem": "Phạm Thị", "ten": "Dung",
        "ngay_sinh": date(1993, 4, 18), "gioi_tinh": "nu",
        "email": "phamthidung@company.vn", "so_dien_thoai": "0934567890",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "doc_than",
        "que_quan": "TP. HCM", "dia_chi_hien_tai": "321 Nguyễn Trãi, Thanh Xuân, HN",
        "luong_co_ban": 12000000, "ngay_vao_lam": date(2021, 2, 1),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKT", "_cv": "NV",
    },
    {
        "ma_dinh_danh": "NV005", "ho_ten_dem": "Hoàng Văn", "ten": "Em",
        "ngay_sinh": date(1988, 9, 30), "gioi_tinh": "nam",
        "email": "hoangvanem@company.vn", "so_dien_thoai": "0945678901",
        "trinh_do_hoc_van": "cao_dang", "tinh_trang_hon_nhan": "da_ket_hon",
        "que_quan": "Thanh Hóa", "dia_chi_hien_tai": "654 Kim Mã, Ba Đình, HN",
        "luong_co_ban": 13000000, "ngay_vao_lam": date(2019, 8, 20),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKT2", "_cv": "KTV",
    },
    {
        "ma_dinh_danh": "NV006", "ho_ten_dem": "Vũ Thị", "ten": "Phương",
        "ngay_sinh": date(1995, 1, 12), "gioi_tinh": "nu",
        "email": "vuthiphuong@company.vn", "so_dien_thoai": "0956789012",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "doc_than",
        "que_quan": "Nghệ An", "dia_chi_hien_tai": "987 Láng Hạ, Đống Đa, HN",
        "luong_co_ban": 11000000, "ngay_vao_lam": date(2022, 4, 10),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKD", "_cv": "NV_KD",
    },
    {
        "ma_dinh_danh": "NV007", "ho_ten_dem": "Đặng Văn", "ten": "Giang",
        "ngay_sinh": date(1983, 6, 25), "gioi_tinh": "nam",
        "email": "dangvangiang@company.vn", "so_dien_thoai": "0967890123",
        "trinh_do_hoc_van": "thac_si", "tinh_trang_hon_nhan": "da_ket_hon",
        "que_quan": "Hà Nam", "dia_chi_hien_tai": "246 Lê Văn Lương, Hà Đông, HN",
        "luong_co_ban": 20000000, "ngay_vao_lam": date(2017, 10, 5),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKT2", "_cv": "TP",
    },
    {
        "ma_dinh_danh": "NV008", "ho_ten_dem": "Bùi Thị", "ten": "Hoa",
        "ngay_sinh": date(1997, 3, 8), "gioi_tinh": "nu",
        "email": "buithihoa@company.vn", "so_dien_thoai": "0978901234",
        "trinh_do_hoc_van": "cao_dang", "tinh_trang_hon_nhan": "doc_than",
        "que_quan": "Hưng Yên", "dia_chi_hien_tai": "135 Hoàng Quốc Việt, Cầu Giấy, HN",
        "luong_co_ban": 10000000, "ngay_vao_lam": date(2023, 1, 15),
        "trang_thai_lam_viec": "thu_viec",
        "_pb": "PHNS", "_cv": "NV",
    },
    {
        "ma_dinh_danh": "NV009", "ho_ten_dem": "Ngô Văn", "ten": "Inh",
        "ngay_sinh": date(1991, 8, 14), "gioi_tinh": "nam",
        "email": "ngovanInh@company.vn", "so_dien_thoai": "0989012345",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "da_ket_hon",
        "que_quan": "Bắc Giang", "dia_chi_hien_tai": "579 Xuân Thủy, Cầu Giấy, HN",
        "luong_co_ban": 16000000, "ngay_vao_lam": date(2018, 5, 20),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKD", "_cv": "PP",
    },
    {
        "ma_dinh_danh": "NV010", "ho_ten_dem": "Lý Thị", "ten": "Kim",
        "ngay_sinh": date(1994, 12, 3), "gioi_tinh": "nu",
        "email": "lythikim@company.vn", "so_dien_thoai": "0901234500",
        "trinh_do_hoc_van": "dai_hoc", "tinh_trang_hon_nhan": "doc_than",
        "que_quan": "Quảng Ninh", "dia_chi_hien_tai": "864 Trần Duy Hưng, Cầu Giấy, HN",
        "luong_co_ban": 14000000, "ngay_vao_lam": date(2021, 9, 1),
        "trang_thai_lam_viec": "dang_lam",
        "_pb": "PHKT", "_cv": "NV",
    },
]

nhan_vien = {}
for d in nhan_vien_data:
    pb_key = d.pop("_pb")
    cv_key = d.pop("_cv")
    existing = env["nhan_vien"].search([("ma_dinh_danh", "=", d["ma_dinh_danh"])], limit=1)
    if existing:
        nv = existing
    else:
        nv = env["nhan_vien"].create(d)
    nhan_vien[d["ma_dinh_danh"]] = nv
    # Tạo lịch sử công tác nếu chưa có
    if not env["lich_su_cong_tac"].search([("nhan_vien_id", "=", nv.id)], limit=1):
        env["lich_su_cong_tac"].create({
            "nhan_vien_id": nv.id,
            "don_vi_id": phong_ban[pb_key].id,
            "chuc_vu_id": chuc_vu[cv_key].id,
            "loai_chuc_vu": "Chính",
        })

print(f"  -> {len(nhan_vien)} nhân viên.")

# Lấy danh sách nhân viên theo mã để dùng tiếp
nv = list(nhan_vien.values())

# --- 4. Hợp đồng lao động ---
print("  Tạo hợp đồng lao động...")
hop_dong_ld_data = [
    {"nhan_vien_id": nv[0].id, "loai_hop_dong": "khong_thoi_han",   "ngay_bat_dau": date(2018, 1, 10), "luong_co_ban": 25000000, "phu_cap_an": 800000, "phu_cap_di_lai": 500000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["BGD"].id},
    {"nhan_vien_id": nv[1].id, "loai_hop_dong": "xac_dinh_thoi_han", "ngay_bat_dau": date(2019, 3, 1),  "ngay_ket_thuc": date(2025, 3, 1),  "luong_co_ban": 18000000, "phu_cap_an": 600000, "phu_cap_di_lai": 400000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHNS"].id},
    {"nhan_vien_id": nv[2].id, "loai_hop_dong": "xac_dinh_thoi_han", "ngay_bat_dau": date(2020, 6, 15), "ngay_ket_thuc": date(2024, 6, 15), "luong_co_ban": 15000000, "phu_cap_an": 500000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKD"].id},
    {"nhan_vien_id": nv[3].id, "loai_hop_dong": "xac_dinh_thoi_han", "ngay_bat_dau": date(2021, 2, 1),  "ngay_ket_thuc": date(2024, 2, 1),  "luong_co_ban": 12000000, "phu_cap_an": 400000, "trang_thai": "het_han", "don_vi_id": phong_ban["PHKT"].id},
    {"nhan_vien_id": nv[4].id, "loai_hop_dong": "khong_thoi_han",   "ngay_bat_dau": date(2019, 8, 20), "luong_co_ban": 13000000, "phu_cap_an": 450000, "phu_cap_di_lai": 300000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKT2"].id},
    {"nhan_vien_id": nv[5].id, "loai_hop_dong": "xac_dinh_thoi_han", "ngay_bat_dau": date(2022, 4, 10), "ngay_ket_thuc": date(2025, 4, 10), "luong_co_ban": 11000000, "phu_cap_an": 400000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKD"].id},
    {"nhan_vien_id": nv[6].id, "loai_hop_dong": "khong_thoi_han",   "ngay_bat_dau": date(2017, 10, 5),  "luong_co_ban": 20000000, "phu_cap_an": 700000, "phu_cap_di_lai": 500000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKT2"].id},
    {"nhan_vien_id": nv[7].id, "loai_hop_dong": "thu_viec",         "ngay_bat_dau": date(2023, 1, 15), "ngay_ket_thuc": date(2023, 7, 15), "luong_co_ban": 10000000, "trang_thai": "het_han", "don_vi_id": phong_ban["PHNS"].id},
    {"nhan_vien_id": nv[8].id, "loai_hop_dong": "khong_thoi_han",   "ngay_bat_dau": date(2018, 5, 20), "luong_co_ban": 16000000, "phu_cap_an": 550000, "phu_cap_di_lai": 400000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKD"].id},
    {"nhan_vien_id": nv[9].id, "loai_hop_dong": "xac_dinh_thoi_han", "ngay_bat_dau": date(2021, 9, 1),  "ngay_ket_thuc": date(2025, 9, 1),  "luong_co_ban": 14000000, "phu_cap_an": 480000, "trang_thai": "hieu_luc", "don_vi_id": phong_ban["PHKT"].id},
]
hop_dong_ld = []
for d in hop_dong_ld_data:
    existing = env["hop_dong_lao_dong"].search([("nhan_vien_id", "=", d["nhan_vien_id"])], limit=1)
    if not existing:
        hop_dong_ld.append(env["hop_dong_lao_dong"].create(d))
    else:
        hop_dong_ld.append(existing)
print(f"  -> {len(hop_dong_ld)} hợp đồng lao động.")

# --- 5. Đơn nghỉ phép ---
print("  Tạo đơn nghỉ phép...")
nghi_phep_data = [
    {"nhan_vien_id": nv[2].id, "loai_nghi": "phep_nam",  "ngay_bat_dau": date(2025, 1, 6),  "ngay_ket_thuc": date(2025, 1, 8),  "ly_do": "Nghỉ phép năm thường niên", "trang_thai": "duyet", "nguoi_duyet_id": nv[1].id},
    {"nhan_vien_id": nv[3].id, "loai_nghi": "om_dau",    "ngay_bat_dau": date(2025, 2, 10), "ngay_ket_thuc": date(2025, 2, 12), "ly_do": "Bị cúm, có giấy bác sĩ", "trang_thai": "duyet", "nguoi_duyet_id": nv[1].id},
    {"nhan_vien_id": nv[5].id, "loai_nghi": "cuoi",      "ngay_bat_dau": date(2025, 3, 20), "ngay_ket_thuc": date(2025, 3, 23), "ly_do": "Tổ chức đám cưới", "trang_thai": "cho_duyet", "nguoi_duyet_id": nv[1].id},
    {"nhan_vien_id": nv[7].id, "loai_nghi": "phep_nam",  "ngay_bat_dau": date(2025, 4, 1),  "ngay_ket_thuc": date(2025, 4, 2),  "ly_do": "Nghỉ phép cuối tuần kéo dài", "trang_thai": "nhap"},
    {"nhan_vien_id": nv[9].id, "loai_nghi": "viec_rieng","ngay_bat_dau": date(2025, 1, 20), "ngay_ket_thuc": date(2025, 1, 21), "ly_do": "Giải quyết việc riêng gia đình", "trang_thai": "tu_choi", "nguoi_duyet_id": nv[0].id, "ly_do_tu_choi": "Thiếu nhân lực trong giai đoạn này"},
]
nghi_phep = []
for d in nghi_phep_data:
    nghi_phep.append(env["nghi_phep"].create(d))
print(f"  -> {len(nghi_phep)} đơn nghỉ phép.")

# --- 6. Bảng lương ---
print("  Tạo bảng lương...")
bang_luong_data = [
    {"nhan_vien_id": nv[0].id, "thang": "1", "nam": 2025, "luong_co_ban": 25000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 800000, "phu_cap_di_lai": 500000, "thuong": 2000000, "so_nguoi_phu_thuoc": 2, "trang_thai": "da_chi"},
    {"nhan_vien_id": nv[1].id, "thang": "1", "nam": 2025, "luong_co_ban": 18000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 600000, "phu_cap_di_lai": 400000, "trang_thai": "da_chi"},
    {"nhan_vien_id": nv[2].id, "thang": "1", "nam": 2025, "luong_co_ban": 15000000, "ngay_cong_thuc_te": 19, "phu_cap_an": 500000, "trang_thai": "xac_nhan"},
    {"nhan_vien_id": nv[4].id, "thang": "1", "nam": 2025, "luong_co_ban": 13000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 450000, "phu_cap_di_lai": 300000, "trang_thai": "da_chi"},
    {"nhan_vien_id": nv[6].id, "thang": "1", "nam": 2025, "luong_co_ban": 20000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 700000, "phu_cap_di_lai": 500000, "thuong": 3000000, "trang_thai": "da_chi"},
    {"nhan_vien_id": nv[0].id, "thang": "2", "nam": 2025, "luong_co_ban": 25000000, "ngay_cong_thuc_te": 20, "phu_cap_an": 800000, "phu_cap_di_lai": 500000, "so_nguoi_phu_thuoc": 2, "trang_thai": "xac_nhan"},
    {"nhan_vien_id": nv[1].id, "thang": "2", "nam": 2025, "luong_co_ban": 18000000, "ngay_cong_thuc_te": 20, "phu_cap_an": 600000, "trang_thai": "nhap"},
    {"nhan_vien_id": nv[8].id, "thang": "1", "nam": 2025, "luong_co_ban": 16000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 550000, "phu_cap_di_lai": 400000, "trang_thai": "da_chi"},
    {"nhan_vien_id": nv[9].id, "thang": "1", "nam": 2025, "luong_co_ban": 14000000, "ngay_cong_thuc_te": 22, "phu_cap_an": 480000, "trang_thai": "xac_nhan"},
    {"nhan_vien_id": nv[3].id, "thang": "1", "nam": 2025, "luong_co_ban": 12000000, "ngay_cong_thuc_te": 20, "phu_cap_an": 400000, "trang_thai": "da_chi"},
]
bang_luong = []
for d in bang_luong_data:
    existing = env["bang_luong"].search([
        ("nhan_vien_id", "=", d["nhan_vien_id"]),
        ("thang", "=", d["thang"]),
        ("nam", "=", d["nam"]),
    ], limit=1)
    if not existing:
        bang_luong.append(env["bang_luong"].create(d))
    else:
        bang_luong.append(existing)
print(f"  -> {len(bang_luong)} bảng lương.")

# --- 7. Đánh giá KPI ---
print("  Tạo đánh giá KPI...")
kpi_data = [
    {"nhan_vien_id": nv[0].id, "nguoi_danh_gia_id": nv[0].id, "ky_danh_gia": "quy", "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "5", "chat_luong": "5", "sang_tao": "4", "lam_viec_nhom": "5", "ky_luat": "5"},
    {"nhan_vien_id": nv[1].id, "nguoi_danh_gia_id": nv[0].id, "ky_danh_gia": "quy", "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "4", "chat_luong": "4", "sang_tao": "3", "lam_viec_nhom": "4", "ky_luat": "5"},
    {"nhan_vien_id": nv[2].id, "nguoi_danh_gia_id": nv[8].id, "ky_danh_gia": "quy", "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "3", "chat_luong": "3", "sang_tao": "4", "lam_viec_nhom": "4", "ky_luat": "4"},
    {"nhan_vien_id": nv[4].id, "nguoi_danh_gia_id": nv[6].id, "ky_danh_gia": "nam",  "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "4", "chat_luong": "5", "sang_tao": "4", "lam_viec_nhom": "4", "ky_luat": "5"},
    {"nhan_vien_id": nv[6].id, "nguoi_danh_gia_id": nv[0].id, "ky_danh_gia": "quy", "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "5", "chat_luong": "5", "sang_tao": "5", "lam_viec_nhom": "5", "ky_luat": "5"},
    {"nhan_vien_id": nv[8].id, "nguoi_danh_gia_id": nv[0].id, "ky_danh_gia": "quy", "quy": "4", "nam": 2024, "hoan_thanh_cong_viec": "4", "chat_luong": "4", "sang_tao": "3", "lam_viec_nhom": "5", "ky_luat": "4"},
]
kpi = []
for d in kpi_data:
    existing = env["danh_gia_kpi"].search([
        ("nhan_vien_id", "=", d["nhan_vien_id"]),
        ("ky_danh_gia", "=", d["ky_danh_gia"]),
        ("quy", "=", d.get("quy")),
        ("nam", "=", d["nam"]),
    ], limit=1)
    if not existing:
        kpi.append(env["danh_gia_kpi"].create(d))
    else:
        kpi.append(existing)
print(f"  -> {len(kpi)} đánh giá KPI.")

# --- 8. Chương trình đào tạo ---
print("  Tạo chương trình đào tạo...")
dao_tao_data = [
    {
        "ten_chuong_trinh": "Kỹ năng lãnh đạo và quản lý nhóm",
        "loai_dao_tao": "ben_ngoai",
        "ngay_bat_dau": date(2025, 3, 10), "ngay_ket_thuc": date(2025, 3, 12),
        "so_gio": 24, "dia_diem": "Khách sạn Melia Hà Nội",
        "giang_vien": "Trung tâm đào tạo Hà Nội Business",
        "chi_phi": 5000000, "trang_thai": "du_kien",
        "nhan_vien_ids": [(6, 0, [nv[1].id, nv[6].id, nv[8].id])],
    },
    {
        "ten_chuong_trinh": "Đào tạo An toàn thông tin cơ bản",
        "loai_dao_tao": "noi_bo",
        "ngay_bat_dau": date(2025, 1, 20), "ngay_ket_thuc": date(2025, 1, 21),
        "so_gio": 16, "dia_diem": "Phòng họp công ty",
        "giang_vien": nv[6].ho_va_ten,
        "chi_phi": 0, "trang_thai": "hoan_thanh",
        "ket_qua": "Toàn bộ nhân viên nắm được các nguyên tắc cơ bản về ATTT",
        "nhan_vien_ids": [(6, 0, [nv[4].id, nv[7].id, nv[9].id])],
    },
    {
        "ten_chuong_trinh": "Kỹ năng bán hàng và chăm sóc khách hàng",
        "loai_dao_tao": "online",
        "ngay_bat_dau": date(2025, 2, 1), "ngay_ket_thuc": date(2025, 2, 28),
        "so_gio": 40, "dia_diem": "Online (Zoom)",
        "giang_vien": "Coursera / Udemy",
        "chi_phi": 2000000, "trang_thai": "dang_dien_ra",
        "nhan_vien_ids": [(6, 0, [nv[2].id, nv[5].id, nv[8].id])],
    },
]
dao_tao_list = []
for d in dao_tao_data:
    existing = env["dao_tao"].search([("ten_chuong_trinh", "=", d["ten_chuong_trinh"])], limit=1)
    if not existing:
        dao_tao_list.append(env["dao_tao"].create(d))
    else:
        dao_tao_list.append(existing)
print(f"  -> {len(dao_tao_list)} chương trình đào tạo.")

# ============================================================
# MODULE KHÁCH HÀNG (CRM)
# ============================================================
print("\n>>> [2/3] MODULE QUẢN LÝ KHÁCH HÀNG")

# --- 9. Khách hàng ---
print("  Tạo khách hàng...")
khach_hang_data = [
    {"ten_khach_hang": "Công ty CP Công nghệ Việt Nam", "loai_khach_hang": "doanh_nghiep", "dia_chi": "Tòa nhà FPT, Láng Hạ, Hà Nội", "dien_thoai": "024 3553 8888", "email": "info@fpt.vn", "ma_so_thue": "0101248141", "nguoi_dai_dien": "Nguyễn Văn Khoa", "chuc_vu_dai_dien": "Giám đốc", "trang_thai": "dang_hop_tac", "nhan_vien_phu_trach_id": nv[2].id},
    {"ten_khach_hang": "Công ty TNHH Thương mại Sao Đỏ", "loai_khach_hang": "doanh_nghiep", "dia_chi": "123 Bà Triệu, Hoàn Kiếm, Hà Nội", "dien_thoai": "024 3825 0001", "email": "contact@saodo.vn", "ma_so_thue": "0100109106", "nguoi_dai_dien": "Trần Thị Mai", "chuc_vu_dai_dien": "Giám đốc điều hành", "trang_thai": "tiem_nang", "nhan_vien_phu_trach_id": nv[5].id},
    {"ten_khach_hang": "Nguyễn Thanh Tùng", "loai_khach_hang": "ca_nhan", "dia_chi": "45 Nguyễn Huệ, Q1, TP. HCM", "dien_thoai": "0912111222", "email": "tung.nt@gmail.com", "gioi_tinh": "nam", "ngay_sinh": date(1988, 5, 20), "trang_thai": "dang_hop_tac", "nhan_vien_phu_trach_id": nv[2].id},
    {"ten_khach_hang": "Công ty CP Đầu tư Bách Việt", "loai_khach_hang": "doanh_nghiep", "dia_chi": "456 Điện Biên Phủ, Q3, TP. HCM", "dien_thoai": "028 3822 1234", "email": "bv@bachviet.com.vn", "ma_so_thue": "0313456789", "nguoi_dai_dien": "Phạm Minh Đức", "chuc_vu_dai_dien": "Tổng Giám đốc", "trang_thai": "dang_hop_tac", "nhan_vien_phu_trach_id": nv[8].id},
    {"ten_khach_hang": "Lê Hoàng Anh", "loai_khach_hang": "ca_nhan", "dia_chi": "78 Võ Văn Tần, Q3, TP. HCM", "dien_thoai": "0923333444", "email": "hoanganh@hotmail.com", "gioi_tinh": "nam", "ngay_sinh": date(1992, 8, 15), "trang_thai": "moi", "nhan_vien_phu_trach_id": nv[5].id},
    {"ten_khach_hang": "Công ty CP Xây dựng Toàn Phát", "loai_khach_hang": "doanh_nghiep", "dia_chi": "789 Tô Hiến Thành, Q10, TP. HCM", "dien_thoai": "028 3955 6677", "email": "info@toanphat.com.vn", "ma_so_thue": "0300900060", "nguoi_dai_dien": "Hoàng Quốc Huy", "chuc_vu_dai_dien": "Giám đốc", "trang_thai": "tam_dung", "nhan_vien_phu_trach_id": nv[8].id},
    {"ten_khach_hang": "Trần Minh Quan", "loai_khach_hang": "ca_nhan", "dia_chi": "12 Lý Thường Kiệt, Hà Nội", "dien_thoai": "0934555666", "email": "tmquan@gmail.com", "gioi_tinh": "nam", "ngay_sinh": date(1985, 3, 10), "trang_thai": "dang_hop_tac", "nhan_vien_phu_trach_id": nv[2].id},
    {"ten_khach_hang": "Công ty TNHH Xuất Nhập Khẩu Nam Anh", "loai_khach_hang": "doanh_nghiep", "dia_chi": "246 Phan Văn Trị, Bình Thạnh, TP. HCM", "dien_thoai": "028 3515 2233", "email": "namanh@namanh.vn", "ma_so_thue": "0304456789", "nguoi_dai_dien": "Vũ Ngọc Anh", "chuc_vu_dai_dien": "Giám đốc", "trang_thai": "tiem_nang", "nhan_vien_phu_trach_id": nv[5].id},
]
khach_hang = []
for d in khach_hang_data:
    existing = env["khach_hang"].search([("ten_khach_hang", "=", d["ten_khach_hang"])], limit=1)
    if not existing:
        khach_hang.append(env["khach_hang"].create(d))
    else:
        khach_hang.append(existing)
print(f"  -> {len(khach_hang)} khách hàng.")

# --- 10. Cơ hội bán hàng ---
print("  Tạo cơ hội bán hàng...")
co_hoi_data = [
    {"ten_co_hoi": "Triển khai hệ thống ERP cho FPT", "khach_hang_id": khach_hang[0].id, "nhan_vien_phu_trach_id": nv[2].id, "nguon_co_hoi": "gioi_thieu", "giai_doan": "dam_phan", "ty_le_thanh_cong": 70.0, "gia_tri_du_kien": 500000000, "ngay_du_kien_chot": date(2025, 6, 30), "mo_ta": "Triển khai hệ thống quản lý nhân sự và kế toán tổng hợp"},
    {"ten_co_hoi": "Tư vấn chuyển đổi số Thương mại Sao Đỏ", "khach_hang_id": khach_hang[1].id, "nhan_vien_phu_trach_id": nv[5].id, "nguon_co_hoi": "email", "giai_doan": "bao_gia", "ty_le_thanh_cong": 40.0, "gia_tri_du_kien": 200000000, "ngay_du_kien_chot": date(2025, 8, 15), "mo_ta": "Tư vấn chiến lược số hóa quy trình kinh doanh"},
    {"ten_co_hoi": "Phần mềm quản lý văn phòng Bách Việt", "khach_hang_id": khach_hang[3].id, "nhan_vien_phu_trach_id": nv[8].id, "nguon_co_hoi": "website", "giai_doan": "thang", "ty_le_thanh_cong": 100.0, "gia_tri_du_kien": 150000000, "ngay_du_kien_chot": date(2025, 2, 28), "ngay_chot_thuc_te": date(2025, 2, 20), "mo_ta": "Triển khai phần mềm quản lý văn bản và hồ sơ"},
    {"ten_co_hoi": "Dịch vụ bảo trì hệ thống CNTT Toàn Phát", "khach_hang_id": khach_hang[5].id, "nhan_vien_phu_trach_id": nv[8].id, "nguon_co_hoi": "dien_thoai", "giai_doan": "thua", "ty_le_thanh_cong": 0.0, "gia_tri_du_kien": 80000000, "ngay_du_kien_chot": date(2024, 12, 31), "ly_do_that_bai": "Khách hàng chọn đối tác khác có giá thấp hơn"},
    {"ten_co_hoi": "Gói phần mềm CRM cho Nam Anh", "khach_hang_id": khach_hang[7].id, "nhan_vien_phu_trach_id": nv[5].id, "nguon_co_hoi": "su_kien", "giai_doan": "du_dieu_kien", "ty_le_thanh_cong": 30.0, "gia_tri_du_kien": 120000000, "ngay_du_kien_chot": date(2025, 9, 30), "mo_ta": "Tư vấn và triển khai CRM cho bộ phận bán hàng"},
]
co_hoi = []
for d in co_hoi_data:
    existing = env["co_hoi_ban_hang"].search([("ten_co_hoi", "=", d["ten_co_hoi"])], limit=1)
    if not existing:
        co_hoi.append(env["co_hoi_ban_hang"].create(d))
    else:
        co_hoi.append(existing)
print(f"  -> {len(co_hoi)} cơ hội bán hàng.")

# --- 11. Báo giá ---
print("  Tạo báo giá...")
bao_gia_data = [
    {"ten_bao_gia": "BG-ERP-FPT-001", "khach_hang_id": khach_hang[0].id, "co_hoi_id": co_hoi[0].id, "tong_gia_tri": 480000000, "nhan_vien_lap_id": nv[2].id, "trang_thai": "gui_khach", "ghi_chu": "Báo giá triển khai ERP giai đoạn 1"},
    {"ten_bao_gia": "BG-CDS-SAODO-001", "khach_hang_id": khach_hang[1].id, "co_hoi_id": co_hoi[1].id, "tong_gia_tri": 195000000, "nhan_vien_lap_id": nv[5].id, "trang_thai": "nhap", "ghi_chu": "Báo giá tư vấn chuyển đổi số"},
    {"ten_bao_gia": "BG-PM-BV-001", "khach_hang_id": khach_hang[3].id, "co_hoi_id": co_hoi[2].id, "tong_gia_tri": 150000000, "nhan_vien_lap_id": nv[8].id, "trang_thai": "khach_dong_y", "ghi_chu": "Báo giá phần mềm văn phòng đã được khách duyệt"},
    {"ten_bao_gia": "BG-CRM-NA-001",  "khach_hang_id": khach_hang[7].id, "co_hoi_id": co_hoi[4].id, "tong_gia_tri": 115000000, "nhan_vien_lap_id": nv[5].id, "trang_thai": "nhap", "ghi_chu": "Dự thảo báo giá CRM lần đầu"},
]
bao_gia = []
for d in bao_gia_data:
    existing = env["bao_gia"].search([("ten_bao_gia", "=", d["ten_bao_gia"])], limit=1)
    if not existing:
        bao_gia.append(env["bao_gia"].create(d))
    else:
        bao_gia.append(existing)
print(f"  -> {len(bao_gia)} báo giá.")

# --- 12. Hợp đồng khách hàng ---
print("  Tạo hợp đồng thương mại...")
hop_dong_kh_data = [
    {"ten_hop_dong": "HĐ Triển khai ERP - FPT 2025", "khach_hang_id": khach_hang[0].id, "loai_hop_dong": "dich_vu", "ngay_ky": date(2025, 3, 1), "ngay_hieu_luc": date(2025, 3, 15), "ngay_het_han": date(2026, 3, 15), "gia_tri": 480000000, "nhan_vien_phu_trach_id": nv[2].id, "trang_thai": "hieu_luc", "co_hoi_id": co_hoi[0].id},
    {"ten_hop_dong": "HĐ Phần mềm quản lý - Bách Việt", "khach_hang_id": khach_hang[3].id, "loai_hop_dong": "dich_vu", "ngay_ky": date(2025, 2, 20), "ngay_hieu_luc": date(2025, 3, 1), "ngay_het_han": date(2026, 2, 28), "gia_tri": 150000000, "nhan_vien_phu_trach_id": nv[8].id, "trang_thai": "hieu_luc", "co_hoi_id": co_hoi[2].id},
    {"ten_hop_dong": "HĐ Bảo trì hàng năm - Nguyễn Thanh Tùng", "khach_hang_id": khach_hang[2].id, "loai_hop_dong": "dich_vu", "ngay_ky": date(2024, 12, 1), "ngay_hieu_luc": date(2025, 1, 1), "ngay_het_han": date(2025, 12, 31), "gia_tri": 36000000, "nhan_vien_phu_trach_id": nv[2].id, "trang_thai": "hieu_luc"},
]
hop_dong_kh = []
for d in hop_dong_kh_data:
    existing = env["hop_dong"].search([("ten_hop_dong", "=", d["ten_hop_dong"])], limit=1)
    if not existing:
        hop_dong_kh.append(env["hop_dong"].create(d))
    else:
        hop_dong_kh.append(existing)
print(f"  -> {len(hop_dong_kh)} hợp đồng thương mại.")

# --- 13. Đơn hàng ---
print("  Tạo đơn hàng...")
don_hang_list = []
don_hang_data = [
    {"ten_don_hang": "Đơn hàng ERP Giai đoạn 1", "khach_hang_id": khach_hang[0].id, "nhan_vien_phu_trach_id": nv[2].id, "ngay_dat": date(2025, 3, 15), "ngay_xac_nhan": date(2025, 3, 16), "trang_thai": "dang_thuc_hien", "hop_dong_id": hop_dong_kh[0].id, "co_hoi_id": co_hoi[0].id, "chi_tiet": [("Phân tích yêu cầu", 1, "Gói", 50000000), ("Thiết kế hệ thống", 1, "Gói", 80000000), ("Lập trình & Cài đặt", 1, "Gói", 200000000)]},
    {"ten_don_hang": "Đơn hàng phần mềm Bách Việt", "khach_hang_id": khach_hang[3].id, "nhan_vien_phu_trach_id": nv[8].id, "ngay_dat": date(2025, 3, 1), "ngay_xac_nhan": date(2025, 3, 2), "ngay_hoan_thanh": date(2025, 3, 30), "trang_thai": "hoan_thanh", "hop_dong_id": hop_dong_kh[1].id, "chi_tiet": [("Cài đặt phần mềm", 1, "Bộ", 120000000), ("Đào tạo sử dụng", 5, "Buổi", 5000000), ("Bảo hành 1 năm", 1, "Năm", 5000000)]},
    {"ten_don_hang": "Dịch vụ bảo trì T3 - Nguyễn Thanh Tùng", "khach_hang_id": khach_hang[2].id, "nhan_vien_phu_trach_id": nv[2].id, "ngay_dat": date(2025, 3, 5), "ngay_xac_nhan": date(2025, 3, 5), "trang_thai": "hoan_thanh", "chi_tiet": [("Bảo trì hệ thống tháng 3", 1, "Tháng", 3000000)]},
    {"ten_don_hang": "Đơn hàng thiết bị CNTT Trần Minh Quan", "khach_hang_id": khach_hang[6].id, "nhan_vien_phu_trach_id": nv[2].id, "ngay_dat": date(2025, 2, 10), "trang_thai": "nhap", "chi_tiet": [("Laptop Dell Latitude 5530", 2, "Chiếc", 25000000), ("Màn hình LG 27 inch", 2, "Chiếc", 8000000)]},
    {"ten_don_hang": "Gói phần mềm khởi điểm - Lê Hoàng Anh", "khach_hang_id": khach_hang[4].id, "nhan_vien_phu_trach_id": nv[5].id, "ngay_dat": date(2025, 1, 20), "ngay_xac_nhan": date(2025, 1, 21), "trang_thai": "xac_nhan", "chi_tiet": [("Phần mềm kế toán cơ bản", 1, "Bản quyền", 15000000), ("Hỗ trợ cài đặt", 1, "Lần", 2000000)]},
]
for d in don_hang_data:
    chi_tiet = d.pop("chi_tiet")
    existing = env["don_hang"].search([("ten_don_hang", "=", d["ten_don_hang"])], limit=1)
    if not existing:
        dh = env["don_hang"].create(d)
        for san_pham, so_luong, dvt, don_gia in chi_tiet:
            env["don_hang_chi_tiet"].create({
                "don_hang_id": dh.id,
                "ten_san_pham": san_pham,
                "so_luong": so_luong,
                "don_vi_tinh": dvt,
                "don_gia": don_gia,
            })
        don_hang_list.append(dh)
    else:
        don_hang_list.append(existing)
print(f"  -> {len(don_hang_list)} đơn hàng.")

# --- 14. Giao hàng ---
print("  Tạo phiếu giao hàng...")
giao_hang_data = [
    {"don_hang_id": don_hang_list[1].id, "dia_chi_giao_hang": "456 Điện Biên Phủ, Q3, TP. HCM", "nguoi_nhan": "Phạm Minh Đức", "so_dien_thoai_nguoi_nhan": "028 3822 1234", "ngay_giao_hang_du_kien": date(2025, 3, 25), "ngay_giao_hang_thuc_te": date(2025, 3, 28), "trang_thai": "da_giao", "don_vi_van_chuyen": "Giao hàng nhanh", "nguoi_ky_nhan": "Phạm Minh Đức", "ngay_ky_nhan": date(2025, 3, 28)},
    {"don_hang_id": don_hang_list[2].id, "dia_chi_giao_hang": "12 Lý Thường Kiệt, Hà Nội", "nguoi_nhan": "Nguyễn Thanh Tùng", "so_dien_thoai_nguoi_nhan": "0912111222", "ngay_giao_hang_du_kien": date(2025, 3, 10), "ngay_giao_hang_thuc_te": date(2025, 3, 10), "trang_thai": "da_giao", "don_vi_van_chuyen": "Kỹ thuật viên tự giao", "nguoi_ky_nhan": "Nguyễn Thanh Tùng", "ngay_ky_nhan": date(2025, 3, 10)},
    {"don_hang_id": don_hang_list[0].id, "dia_chi_giao_hang": "Tòa nhà FPT, Láng Hạ, Hà Nội", "nguoi_nhan": "Nguyễn Văn Khoa", "so_dien_thoai_nguoi_nhan": "024 3553 8888", "ngay_giao_hang_du_kien": date(2025, 6, 1), "trang_thai": "chuan_bi", "don_vi_van_chuyen": "Tự giao"},
]
giao_hang_list = []
for d in giao_hang_data:
    existing = env["giao_hang"].search([("don_hang_id", "=", d["don_hang_id"])], limit=1)
    if not existing:
        giao_hang_list.append(env["giao_hang"].create(d))
    else:
        giao_hang_list.append(existing)
print(f"  -> {len(giao_hang_list)} phiếu giao hàng.")

# --- 15. Hóa đơn ---
print("  Tạo hóa đơn...")
hoa_don_data = [
    {"khach_hang_id": khach_hang[3].id, "don_hang_id": don_hang_list[1].id, "ngay_xuat": date(2025, 3, 30), "han_thanh_toan": date(2025, 4, 29), "thue_vat": 10.0, "_trang_thai": "da_thanh_toan", "chi_tiet": [("Cài đặt phần mềm", 1, 120000000), ("Đào tạo sử dụng (5 buổi)", 5, 5000000), ("Bảo hành 1 năm", 1, 5000000)]},
    {"khach_hang_id": khach_hang[2].id, "don_hang_id": don_hang_list[2].id, "ngay_xuat": date(2025, 3, 31), "han_thanh_toan": date(2025, 4, 15), "thue_vat": 10.0, "_trang_thai": "da_thanh_toan", "chi_tiet": [("Bảo trì hệ thống tháng 3", 1, 3000000)]},
    {"khach_hang_id": khach_hang[0].id, "don_hang_id": don_hang_list[0].id, "ngay_xuat": date(2025, 4, 1),  "han_thanh_toan": date(2025, 5, 1),  "thue_vat": 10.0, "_trang_thai": "da_xuat",    "chi_tiet": [("Phân tích yêu cầu", 1, 50000000), ("Thiết kế hệ thống", 1, 80000000)]},
    {"khach_hang_id": khach_hang[4].id, "don_hang_id": don_hang_list[4].id, "ngay_xuat": date(2025, 1, 25), "han_thanh_toan": date(2025, 2, 24), "thue_vat": 10.0, "_trang_thai": "qua_han",  "chi_tiet": [("Phần mềm kế toán cơ bản", 1, 15000000), ("Hỗ trợ cài đặt", 1, 2000000)]},
]
hoa_don_list = []
for d in hoa_don_data:
    chi_tiet = d.pop("chi_tiet")
    target_trang_thai = d.pop("_trang_thai")
    existing = env["hoa_don"].search([
        ("khach_hang_id", "=", d["khach_hang_id"]),
        ("ngay_xuat", "=", d["ngay_xuat"]),
    ], limit=1)
    if not existing:
        hd = env["hoa_don"].create(d)
        for ten, sl, don_gia in chi_tiet:
            env["hoa_don_chi_tiet"].create({
                "hoa_don_id": hd.id,
                "ten_san_pham": ten,
                "so_luong": sl,
                "don_gia": don_gia,
            })
        # Xuất hóa đơn: xuat để kích hoạt workflow
        if target_trang_thai in ('da_xuat', 'da_thanh_toan', 'qua_han'):
            try:
                hd.action_xuat_hoa_don()
            except Exception:
                pass
        hoa_don_list.append(hd)
    else:
        hoa_don_list.append(existing)
print(f"  -> {len(hoa_don_list)} hóa đơn.")

# --- 16. Thanh toán ---
print("  Tạo thanh toán...")
thanh_toan_data = [
    # Hóa đơn Bách Việt: tong = 150tr, VAT 10% -> 165tr -> thanh toán đủ -> da_thanh_toan
    {"hoa_don_id": hoa_don_list[0].id, "so_tien": 165000000, "ngay_thanh_toan": date(2025, 4, 20), "hinh_thuc": "chuyen_khoan", "ten_ngan_hang": "Vietcombank", "trang_thai": "da_xac_nhan", "ghi_chu": "Thanh toán 100% hóa đơn phần mềm Bách Việt"},
    # Hóa đơn bảo trì Nguyễn Thanh Tùng: tong = 3tr, VAT 10% -> 3.3tr -> da_thanh_toan
    {"hoa_don_id": hoa_don_list[1].id, "so_tien": 3300000, "ngay_thanh_toan": date(2025, 4, 10), "hinh_thuc": "chuyen_khoan", "ten_ngan_hang": "Techcombank", "trang_thai": "da_xac_nhan", "ghi_chu": "Thanh toán dịch vụ bảo trì tháng 3"},
    # Hóa đơn FPT: tong = 130tr+VAT=143tr -> thanh toán 1 phần, cho_xac_nhan -> stays da_xuat
    {"hoa_don_id": hoa_don_list[2].id, "so_tien": 66000000, "ngay_thanh_toan": date(2025, 4, 28), "hinh_thuc": "chuyen_khoan", "ten_ngan_hang": "BIDV", "trang_thai": "cho_xac_nhan", "ghi_chu": "Thanh toán đợt 1 - FPT ERP"},
]
thanh_toan_list = []
for d in thanh_toan_data:
    existing = env["thanh_toan"].search([("hoa_don_id", "=", d["hoa_don_id"])], limit=1)
    if not existing:
        thanh_toan_list.append(env["thanh_toan"].create(d))
    else:
        thanh_toan_list.append(existing)
print(f"  -> {len(thanh_toan_list)} thanh toán.")

# --- 17. Khiếu nại ---
print("  Tạo khiếu nại...")
khieu_nai_data = [
    {"tieu_de": "Lỗi hiển thị báo cáo trên phần mềm", "khach_hang_id": khach_hang[3].id, "loai": "san_pham", "do_uu_tien": "cao", "nguoi_xu_ly_id": nv[4].id, "trang_thai": "dang_xu_ly", "han_xu_ly": date(2025, 4, 10)},
    {"tieu_de": "Giao hàng chậm so với cam kết", "khach_hang_id": khach_hang[2].id, "loai": "giao_hang", "do_uu_tien": "trung_binh", "nguoi_xu_ly_id": nv[8].id, "trang_thai": "da_giai_quyet", "ngay_giai_quyet": date(2025, 3, 15)},
]
for d in khieu_nai_data:
    existing = env["khieu_nai_phan_hoi"].search([("tieu_de", "=", d["tieu_de"])], limit=1)
    if not existing:
        env["khieu_nai_phan_hoi"].create(d)
print("  -> 2 khiếu nại.")

# ============================================================
# MODULE QUẢN LÝ VĂN BẢN
# ============================================================
print("\n>>> [3/3] MODULE QUẢN LÝ VĂN BẢN")

# --- 18. Loại văn bản ---
print("  Tạo loại văn bản...")
loai_vb_data = [
    {"ma_loai": "QD",  "ten_loai": "Quyết định",          "mo_ta": "Văn bản quyết định của cơ quan, tổ chức"},
    {"ma_loai": "CV",  "ten_loai": "Công văn",             "mo_ta": "Công văn trao đổi nghiệp vụ"},
    {"ma_loai": "TB",  "ten_loai": "Thông báo",            "mo_ta": "Thông báo nội bộ và bên ngoài"},
    {"ma_loai": "BC",  "ten_loai": "Báo cáo",              "mo_ta": "Báo cáo định kỳ và đột xuất"},
    {"ma_loai": "HD",  "ten_loai": "Hợp đồng",             "mo_ta": "Hợp đồng kinh tế và lao động"},
    {"ma_loai": "BB",  "ten_loai": "Biên bản",             "mo_ta": "Biên bản họp, kiểm tra, xác nhận"},
    {"ma_loai": "GUX", "ten_loai": "Giấy ủy quyền",        "mo_ta": "Giấy ủy quyền thực hiện công việc"},
]
loai_vb = {}
for d in loai_vb_data:
    existing = env["loai_van_ban"].search([("ma_loai", "=", d["ma_loai"])], limit=1)
    if existing:
        loai_vb[d["ma_loai"]] = existing
    else:
        loai_vb[d["ma_loai"]] = env["loai_van_ban"].create(d)
print(f"  -> {len(loai_vb)} loại văn bản.")

# --- 19. Sổ công văn ---
print("  Tạo sổ công văn...")
scv_den = env["so_cong_van"].search([("loai_so", "=", "den"), ("nam", "=", 2025)], limit=1)
if not scv_den:
    scv_den = env["so_cong_van"].create({
        "ten_so": "Sổ công văn đến năm 2025",
        "loai_so": "den",
        "nam": 2025,
        "don_vi_id": phong_ban["PHNS"].id,
        "nguoi_quan_ly_id": nv[1].id,
        "trang_thai": "mo",
    })
scv_di = env["so_cong_van"].search([("loai_so", "=", "di"), ("nam", "=", 2025)], limit=1)
if not scv_di:
    scv_di = env["so_cong_van"].create({
        "ten_so": "Sổ công văn đi năm 2025",
        "loai_so": "di",
        "nam": 2025,
        "don_vi_id": phong_ban["PHNS"].id,
        "nguoi_quan_ly_id": nv[1].id,
        "trang_thai": "mo",
    })
print("  -> 2 sổ công văn.")

# --- 20. Văn bản đến ---
print("  Tạo văn bản đến...")
van_ban_den_data = [
    {"so_ky_hieu": "VBD-2025-001", "ngay_den": date(2025, 1, 5),  "ngay_van_ban": date(2025, 1, 3),  "noi_ban_hanh": "Bộ Thông tin và Truyền thông", "trich_yeu": "Thông báo về quy định an toàn thông tin mạng 2025", "loai_van_ban_id": loai_vb["TB"].id, "do_khan": "thuong", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[6].id, "han_xu_ly": date(2025, 2, 5), "trang_thai": "da_xu_ly"},
    {"so_ky_hieu": "VBD-2025-002", "ngay_den": date(2025, 1, 15), "ngay_van_ban": date(2025, 1, 12), "noi_ban_hanh": "Sở Kế hoạch và Đầu tư Hà Nội", "trich_yeu": "Yêu cầu nộp báo cáo tình hình hoạt động doanh nghiệp năm 2024", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "khan", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[3].id, "han_xu_ly": date(2025, 1, 31), "trang_thai": "da_xu_ly", "da_ky_duyet": True, "ngay_ky_duyet": date(2025, 1, 16)},
    {"so_ky_hieu": "VBD-2025-003", "ngay_den": date(2025, 2, 10), "ngay_van_ban": date(2025, 2, 8),  "noi_ban_hanh": "Công ty CP Công nghệ Việt Nam (FPT)", "trich_yeu": "Yêu cầu bổ sung tài liệu dự án ERP giai đoạn 1", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "khan", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[2].id, "han_xu_ly": date(2025, 2, 20), "trang_thai": "dang_xu_ly", "khach_hang_id": khach_hang[0].id},
    {"so_ky_hieu": "VBD-2025-004", "ngay_den": date(2025, 3, 1),  "ngay_van_ban": date(2025, 2, 28), "noi_ban_hanh": "Cục Thuế Hà Nội", "trich_yeu": "Thông báo kiểm tra thuế định kỳ tháng 3/2025", "loai_van_ban_id": loai_vb["TB"].id, "do_khan": "hoa_toc", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[3].id, "han_xu_ly": date(2025, 3, 10), "trang_thai": "moi"},
    {"so_ky_hieu": "VBD-2025-005", "ngay_den": date(2025, 3, 15), "ngay_van_ban": date(2025, 3, 12), "noi_ban_hanh": "Bộ Lao động - Thương binh và Xã hội", "trich_yeu": "Hướng dẫn thực hiện chính sách bảo hiểm thất nghiệp 2025", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "thuong", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[1].id, "trang_thai": "dang_xu_ly"},
    {"so_ky_hieu": "VBD-2025-006", "ngay_den": date(2025, 4, 2),  "ngay_van_ban": date(2025, 3, 30), "noi_ban_hanh": "Công ty TNHH Thương mại Sao Đỏ", "trich_yeu": "Phản hồi báo giá tư vấn chuyển đổi số - yêu cầu thương lượng thêm", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "thuong", "so_cong_van_id": scv_den.id, "nguoi_xu_ly_id": nv[5].id, "trang_thai": "moi", "khach_hang_id": khach_hang[1].id},
]
vbd_list = []
for d in van_ban_den_data:
    existing = env["van_ban_den"].search([("so_ky_hieu", "=", d["so_ky_hieu"])], limit=1)
    if not existing:
        vbd_list.append(env["van_ban_den"].create(d))
    else:
        vbd_list.append(existing)
print(f"  -> {len(vbd_list)} văn bản đến.")

# --- 21. Văn bản đi ---
print("  Tạo văn bản đi...")
van_ban_di_data = [
    {"so_ky_hieu": "VBI-2025-001", "ngay_van_ban": date(2025, 1, 10), "ngay_gui": date(2025, 1, 11), "noi_nhan": "Sở Kế hoạch và Đầu tư Hà Nội", "nguoi_ky": "Nguyễn Văn An - Giám đốc", "trich_yeu": "Báo cáo tình hình hoạt động doanh nghiệp năm 2024", "loai_van_ban_id": loai_vb["BC"].id, "do_khan": "khan", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[3].id, "don_vi_soan_thao_id": phong_ban["PHKT"].id, "approver_tp_id": nv[1].id, "approver_gd_id": nv[0].id, "tp_da_duyet": True, "tp_ngay_duyet": date(2025, 1, 9), "gd_da_duyet": True, "gd_ngay_duyet": date(2025, 1, 10), "trang_thai": "da_gui"},
    {"so_ky_hieu": "VBI-2025-002", "ngay_van_ban": date(2025, 2, 1),  "ngay_gui": date(2025, 2, 3),  "noi_nhan": "Công ty CP Công nghệ Việt Nam (FPT)", "nguoi_ky": "Nguyễn Văn An - Giám đốc", "trich_yeu": "Gửi hồ sơ năng lực và đề xuất triển khai ERP", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "thuong", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[2].id, "don_vi_soan_thao_id": phong_ban["PHKD"].id, "approver_tp_id": nv[8].id, "approver_gd_id": nv[0].id, "tp_da_duyet": True, "tp_ngay_duyet": date(2025, 1, 30), "gd_da_duyet": True, "gd_ngay_duyet": date(2025, 2, 1), "trang_thai": "hoan_tat", "khach_hang_id": khach_hang[0].id},
    {"so_ky_hieu": "VBI-2025-003", "ngay_van_ban": date(2025, 2, 15), "noi_nhan": "Toàn thể cán bộ nhân viên", "nguoi_ky": "Trần Thị Bình - Trưởng phòng NS", "trich_yeu": "Thông báo lịch nghỉ Tết Nguyên Đán và điều chỉnh ngày làm bù 2025", "loai_van_ban_id": loai_vb["TB"].id, "do_khan": "thuong", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[1].id, "don_vi_soan_thao_id": phong_ban["PHNS"].id, "approver_tp_id": nv[1].id, "approver_gd_id": nv[0].id, "tp_da_duyet": True, "tp_ngay_duyet": date(2025, 2, 14), "gd_da_duyet": True, "gd_ngay_duyet": date(2025, 2, 15), "trang_thai": "da_gui"},
    {"so_ky_hieu": "VBI-2025-004", "ngay_van_ban": date(2025, 3, 5),  "noi_nhan": "Công ty TNHH Thương mại Sao Đỏ", "nguoi_ky": "Lê Minh Cường - NV Kinh doanh", "trich_yeu": "Gửi báo giá dịch vụ tư vấn chuyển đổi số (lần 1)", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "thuong", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[5].id, "don_vi_soan_thao_id": phong_ban["PHKD"].id, "approver_tp_id": nv[8].id, "trang_thai": "cho_duyet", "khach_hang_id": khach_hang[1].id},
    {"so_ky_hieu": "VBI-2025-005", "ngay_van_ban": date(2025, 3, 20), "noi_nhan": "Cục Thuế Hà Nội", "nguoi_ky": "Nguyễn Văn An - Giám đốc", "trich_yeu": "Báo cáo giải trình số liệu quyết toán thuế TNDN năm 2024", "loai_van_ban_id": loai_vb["BC"].id, "do_khan": "hoa_toc", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[3].id, "don_vi_soan_thao_id": phong_ban["PHKT"].id, "approver_tp_id": nv[1].id, "approver_gd_id": nv[0].id, "tp_da_duyet": True, "tp_ngay_duyet": date(2025, 3, 19), "gd_da_duyet": True, "gd_ngay_duyet": date(2025, 3, 20), "trang_thai": "da_gui"},
    {"so_ky_hieu": "VBI-2025-006", "ngay_van_ban": date(2025, 4, 1),  "noi_nhan": "Bộ Lao động TB&XH", "nguoi_ky": "Trần Thị Bình - Trưởng phòng NS", "trich_yeu": "Phản hồi và yêu cầu giải thích thêm về hướng dẫn BHTN 2025", "loai_van_ban_id": loai_vb["CV"].id, "do_khan": "thuong", "so_cong_van_id": scv_di.id, "nguoi_soan_thao_id": nv[1].id, "don_vi_soan_thao_id": phong_ban["PHNS"].id, "trang_thai": "du_thao"},
]
vbi_list = []
for d in van_ban_di_data:
    existing = env["van_ban_di"].search([("so_ky_hieu", "=", d["so_ky_hieu"])], limit=1)
    if not existing:
        vbi_list.append(env["van_ban_di"].create(d))
    else:
        vbi_list.append(existing)
print(f"  -> {len(vbi_list)} văn bản đi.")

# ============================================================
# Commit
# ============================================================
env.cr.commit()

print("\n" + "=" * 60)
print("HOÀN THÀNH TẠO DỮ LIỆU MẪU!")
print("=" * 60)
print("""
Tóm tắt dữ liệu đã tạo:
MODULE NHÂN SỰ:
  - 5 phòng ban / đơn vị
  - 7 chức vụ
  - 10 nhân viên (kèm lịch sử công tác)
  - 10 hợp đồng lao động (nhiều loại, nhiều trạng thái)
  - 5 đơn nghỉ phép (duyệt, chờ duyệt, từ chối, nháp)
  - 10 bảng lương (đã chi, đã xác nhận, nháp)
  - 6 đánh giá KPI (theo quý và năm)
  - 3 chương trình đào tạo

MODULE KHÁCH HÀNG (CRM):
  - 8 khách hàng (cá nhân & doanh nghiệp, nhiều trạng thái)
  - 5 cơ hội bán hàng (đủ các giai đoạn)
  - 4 báo giá
  - 3 hợp đồng thương mại
  - 5 đơn hàng (kèm chi tiết sản phẩm)
  - 3 phiếu giao hàng
  - 4 hóa đơn (đã thanh toán, chờ, quá hạn)
  - 3 thanh toán
  - 2 khiếu nại

MODULE VĂN BẢN:
  - 7 loại văn bản
  - 2 sổ công văn (sổ đến & sổ đi 2025)
  - 6 văn bản đến (mới, đang xử lý, đã xử lý)
  - 6 văn bản đi (dự thảo, chờ duyệt, đã duyệt, đã gửi, hoàn tất)
""")
