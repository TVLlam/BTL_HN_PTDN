"""
Script tạo dữ liệu test cho hệ thống ERP - CNTT17-07-NHOM4
Chạy qua: python3 odoo-bin shell --config=odoo.conf -d tranvanlam --no-http < tao_du_lieu_test.py
"""
from datetime import date, timedelta

print("=" * 60)
print("BẮT ĐẦU TẠO DỮ LIỆU TEST ERP")
print("=" * 60)

# ─────────────────────────────────────────────
# 0. CHỨC VỤ & ĐƠN VỊ (prerequisites)
# ─────────────────────────────────────────────
def lay_tao_chuc_vu(ma, ten, cap_do=1):
    r = env['chuc_vu'].sudo().search([('ten_chuc_vu', '=', ten)], limit=1)
    if r: return r.id
    return env['chuc_vu'].sudo().create({'ma_chuc_vu': ma, 'ten_chuc_vu': ten, 'cap_do': cap_do}).id

def lay_tao_don_vi(ma, ten, cap_do=1):
    r = env['don_vi'].sudo().search([('ten_don_vi', '=', ten)], limit=1)
    if r: return r.id
    return env['don_vi'].sudo().create({'ma_don_vi': ma, 'ten_don_vi': ten, 'cap_do': cap_do}).id

cv_nv_kt      = lay_tao_chuc_vu('CV001', 'Nhân viên Kỹ thuật', 1)
cv_nv_pm      = lay_tao_chuc_vu('CV002', 'Nhân viên Phát triển phần mềm', 1)
cv_tp_mkt     = lay_tao_chuc_vu('CV003', 'Trưởng phòng Marketing', 3)
cv_gd_kd      = lay_tao_chuc_vu('CV004', 'Giám đốc Kinh doanh', 4)
cv_nv_kt_acc  = lay_tao_chuc_vu('CV005', 'Nhân viên Kế toán', 1)
print(f"[0/4] Chức vụ & Đơn vị đã chuẩn bị xong")

dv_kt   = lay_tao_don_vi('DV001', 'Phòng Kỹ thuật - Công nghệ', 2)
dv_cntt = lay_tao_don_vi('DV002', 'Phòng Công nghệ thông tin', 2)
dv_mkt  = lay_tao_don_vi('DV003', 'Phòng Marketing & Truyền thông', 2)
dv_bgd  = lay_tao_don_vi('DV004', 'Ban Giám Đốc', 4)
dv_ktc  = lay_tao_don_vi('DV005', 'Phòng Tài chính - Kế toán', 2)

# ─────────────────────────────────────────────
# 1. NHÂN VIÊN
# ─────────────────────────────────────────────
print("\n[1/4] Tạo nhân viên...")

danh_sach_nhan_vien = [
    {
        'ma_dinh_danh': 'NV20220301',
        'ho_ten_dem': 'Dương Ngọc',
        'ten': 'Đông',
        'gioi_tinh': 'nam',
        'ngay_sinh': '1995-04-12',
        'so_cmnd_cccd': '036095012345',
        'ngay_cap_cccd': '2021-01-15',
        'noi_cap_cccd': 'Cục Cảnh sát ĐKQL cư trú và DLQG về dân cư',
        'que_quan': 'Hà Nội',
        'dia_chi_hien_tai': '45 Nguyễn Huệ, Quận 1, TP.HCM',
        'email': 'duong.ngoc.dong@company.vn',
        'so_dien_thoai': '0901234567',
        'trinh_do_hoc_van': 'dai_hoc',
        'tinh_trang_hon_nhan': 'doc_than',
        'dan_toc': 'Kinh',
        'ton_giao': 'Không',
        'so_tai_khoan_ngan_hang': '19038012345678',
        'ten_ngan_hang': 'Techcombank',
        'ngay_vao_lam': '2022-03-01',
        'trang_thai_lam_viec': 'dang_lam',
        'luong_co_ban': 12000000,
        'chuc_vu_hien_tai': cv_nv_kt,
        'don_vi_hien_tai': dv_kt,
    },
    {
        'ma_dinh_danh': 'NV20230110',
        'ho_ten_dem': 'Trần Văn',
        'ten': 'Lâm',
        'gioi_tinh': 'nam',
        'ngay_sinh': '1998-07-25',
        'so_cmnd_cccd': '079098054321',
        'ngay_cap_cccd': '2020-06-20',
        'noi_cap_cccd': 'Cục Cảnh sát ĐKQL cư trú và DLQG về dân cư',
        'que_quan': 'TP. Hồ Chí Minh',
        'dia_chi_hien_tai': '123 Lê Lợi, Quận 3, TP.HCM',
        'email': 'tran.van.lam@company.vn',
        'so_dien_thoai': '0912345678',
        'trinh_do_hoc_van': 'dai_hoc',
        'tinh_trang_hon_nhan': 'doc_than',
        'dan_toc': 'Kinh',
        'ton_giao': 'Không',
        'so_tai_khoan_ngan_hang': '19038087654321',
        'ten_ngan_hang': 'Vietcombank',
        'ngay_vao_lam': '2023-01-10',
        'trang_thai_lam_viec': 'dang_lam',
        'luong_co_ban': 10000000,
        'chuc_vu_hien_tai': cv_nv_pm,
        'don_vi_hien_tai': dv_cntt,
    },
    {
        'ma_dinh_danh': 'NV20210815',
        'ho_ten_dem': 'Nguyễn Thị Thanh',
        'ten': 'Nhã',
        'gioi_tinh': 'nu',
        'ngay_sinh': '1997-11-08',
        'so_cmnd_cccd': '079097098765',
        'ngay_cap_cccd': '2019-11-25',
        'noi_cap_cccd': 'Cục Cảnh sát ĐKQL cư trú và DLQG về dân cư',
        'que_quan': 'Đà Nẵng',
        'dia_chi_hien_tai': '56 Trần Phú, Quận Hải Châu, Đà Nẵng',
        'email': 'nguyen.thanh.nha@company.vn',
        'so_dien_thoai': '0923456789',
        'trinh_do_hoc_van': 'thac_si',
        'tinh_trang_hon_nhan': 'da_ket_hon',
        'dan_toc': 'Kinh',
        'ton_giao': 'Phật giáo',
        'so_tai_khoan_ngan_hang': '19038011223344',
        'ten_ngan_hang': 'BIDV',
        'ngay_vao_lam': '2021-08-15',
        'trang_thai_lam_viec': 'dang_lam',
        'luong_co_ban': 14000000,
        'chuc_vu_hien_tai': cv_tp_mkt,
        'don_vi_hien_tai': dv_mkt,
    },
    {
        'ma_dinh_danh': 'NV20190501',
        'ho_ten_dem': 'Lê Minh',
        'ten': 'Tuấn',
        'gioi_tinh': 'nam',
        'ngay_sinh': '1990-02-14',
        'so_cmnd_cccd': '001090044556',
        'ngay_cap_cccd': '2018-05-10',
        'noi_cap_cccd': 'Công an TP. Hà Nội',
        'que_quan': 'Hải Phòng',
        'dia_chi_hien_tai': '78 Giải Phóng, Hai Bà Trưng, Hà Nội',
        'email': 'le.minh.tuan@company.vn',
        'so_dien_thoai': '0934567890',
        'trinh_do_hoc_van': 'dai_hoc',
        'tinh_trang_hon_nhan': 'da_ket_hon',
        'dan_toc': 'Kinh',
        'ton_giao': 'Không',
        'so_tai_khoan_ngan_hang': '19038099887766',
        'ten_ngan_hang': 'MB Bank',
        'ngay_vao_lam': '2019-05-01',
        'trang_thai_lam_viec': 'dang_lam',
        'luong_co_ban': 18000000,
        'chuc_vu_hien_tai': cv_gd_kd,
        'don_vi_hien_tai': dv_bgd,
    },
    {
        'ma_dinh_danh': 'NV20220901',
        'ho_ten_dem': 'Phạm Thị',
        'ten': 'Hương',
        'gioi_tinh': 'nu',
        'ngay_sinh': '1994-09-30',
        'so_cmnd_cccd': '038094067890',
        'ngay_cap_cccd': '2022-03-08',
        'noi_cap_cccd': 'Cục Cảnh sát ĐKQL cư trú và DLQG về dân cư',
        'que_quan': 'Long An',
        'dia_chi_hien_tai': '200 Nguyễn Văn Linh, Bình Chánh, TP.HCM',
        'email': 'pham.thi.huong@company.vn',
        'so_dien_thoai': '0945678901',
        'trinh_do_hoc_van': 'dai_hoc',
        'tinh_trang_hon_nhan': 'doc_than',
        'dan_toc': 'Kinh',
        'ton_giao': 'Không',
        'so_tai_khoan_ngan_hang': '19038055443322',
        'ten_ngan_hang': 'Agribank',
        'ngay_vao_lam': '2022-09-01',
        'trang_thai_lam_viec': 'dang_lam',
        'luong_co_ban': 11000000,
        'chuc_vu_hien_tai': cv_nv_kt_acc,
        'don_vi_hien_tai': dv_ktc,
    },
]

nhan_vien_records = []
for nv_data in danh_sach_nhan_vien:
    existing = env['nhan_vien'].sudo().search([('email', '=', nv_data['email'])], limit=1)
    if existing:
        nhan_vien_records.append(existing)
        print(f"  ✓ (đã có) {nv_data['ho_ten_dem']} {nv_data['ten']}")
    else:
        nv = env['nhan_vien'].sudo().create(nv_data)
        nhan_vien_records.append(nv)
        print(f"  ✓ Tạo: {nv.ho_va_ten} (ID: {nv.id})")

# ─────────────────────────────────────────────
# 2. KHÁCH HÀNG
# ─────────────────────────────────────────────
print("\n[2/4] Tạo khách hàng...")

danh_sach_khach_hang = [
    {
        'ten_khach_hang': 'Công ty TNHH Phần mềm TechSoft Việt Nam',
        'loai_khach_hang': 'doanh_nghiep',
        'dia_chi': 'Tầng 8, Tòa nhà Viettel, 285 Cách Mạng Tháng 8, Quận 10, TP.HCM',
        'dien_thoai': '028 3838 9999',
        'email': 'contact@techsoft.vn',
    },
    {
        'ten_khach_hang': 'Tập đoàn Bách Khoa Việt Nam',
        'loai_khach_hang': 'doanh_nghiep',
        'dia_chi': '268 Lý Thường Kiệt, Phường 14, Quận 10, TP.HCM',
        'dien_thoai': '028 3865 4321',
        'email': 'info@bachkhoa.vn',
    },
    {
        'ten_khach_hang': 'Công ty Cổ phần Thương mại Minh Châu',
        'loai_khach_hang': 'doanh_nghiep',
        'dia_chi': '45 Đinh Tiên Hoàng, Quận Bình Thạnh, TP.HCM',
        'dien_thoai': '028 3556 7788',
        'email': 'minchau@minhchau.com.vn',
    },
    {
        'ten_khach_hang': 'Tổng công ty Điện lực Miền Nam',
        'loai_khach_hang': 'doanh_nghiep',
        'dia_chi': '72 Hai Bà Trưng, Quận 1, TP.HCM',
        'dien_thoai': '028 3914 1000',
        'email': 'evnspc@evnspc.vn',
    },
    {
        'ten_khach_hang': 'Ông Nguyễn Thanh Bình',
        'loai_khach_hang': 'ca_nhan',
        'dia_chi': '12 Nguyễn Đình Chiểu, Quận 3, TP.HCM',
        'dien_thoai': '0901112233',
        'email': 'nguyen.binh@gmail.com',
    },
    {
        'ten_khach_hang': 'Bà Trần Thị Mai Anh',
        'loai_khach_hang': 'ca_nhan',
        'dia_chi': '88 Bùi Thị Xuân, Quận 1, TP.HCM',
        'dien_thoai': '0912223344',
        'email': 'maianh.tran@gmail.com',
    },
    {
        'ten_khach_hang': 'Công ty TNHH Xây dựng Hoàng Gia',
        'loai_khach_hang': 'doanh_nghiep',
        'dia_chi': '156 Hoàng Diệu 2, Thủ Đức, TP.HCM',
        'dien_thoai': '028 3726 5544',
        'email': 'hoanggia@xaydung.vn',
    },
]

khach_hang_records = []
for kh_data in danh_sach_khach_hang:
    existing = env['khach_hang'].sudo().search([('ten_khach_hang', '=', kh_data['ten_khach_hang'])], limit=1)
    if existing:
        khach_hang_records.append(existing)
        print(f"  ✓ (đã có) {kh_data['ten_khach_hang']}")
    else:
        kh = env['khach_hang'].sudo().create(kh_data)
        khach_hang_records.append(kh)
        print(f"  ✓ Tạo: {kh.ten_khach_hang} (ID: {kh.id})")

# ─────────────────────────────────────────────
# 3. HỢP ĐỒNG
# ─────────────────────────────────────────────
print("\n[3/4] Tạo hợp đồng...")

# Lấy nhân viên phụ trách
nv_dong = nhan_vien_records[0]   # Dương Ngọc Đông
nv_lam = nhan_vien_records[1]    # Trần Văn Lâm
nv_nha = nhan_vien_records[2]    # Nguyễn Thị Thanh Nhã
nv_tuan = nhan_vien_records[3]   # Lê Minh Tuấn

kh_techsoft = khach_hang_records[0]
kh_bachkhoa = khach_hang_records[1]
kh_minhchau = khach_hang_records[2]
kh_dien_luc = khach_hang_records[3]
kh_hoang_gia = khach_hang_records[6]

danh_sach_hop_dong = [
    {
        'ma_hop_dong': 'HD-2025-001',
        'ten_hop_dong': 'Hợp đồng cung cấp phần mềm quản lý nhân sự',
        'khach_hang_id': kh_techsoft.id,
        'loai_hop_dong': 'dich_vu',
        'ngay_ky': '2025-01-15',
        'ngay_hieu_luc': '2025-02-01',
        'ngay_het_han': '2026-01-31',
        'gia_tri': 350000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_lam.id,
        'trang_thai': 'hieu_luc',
        'mo_ta': 'Hợp đồng cung cấp và triển khai phần mềm quản lý nhân sự tích hợp ERP cho TechSoft Việt Nam. Bao gồm: cài đặt, đào tạo, hỗ trợ kỹ thuật 12 tháng.',
    },
    {
        'ma_hop_dong': 'HD-2025-002',
        'ten_hop_dong': 'Hợp đồng tư vấn và triển khai hệ thống ERP',
        'khach_hang_id': kh_bachkhoa.id,
        'loai_hop_dong': 'dich_vu',
        'ngay_ky': '2025-03-10',
        'ngay_hieu_luc': '2025-04-01',
        'ngay_het_han': '2027-03-31',
        'gia_tri': 1200000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_tuan.id,
        'trang_thai': 'hieu_luc',
        'mo_ta': 'Tư vấn, thiết kế và triển khai hệ thống ERP tổng thể cho Tập đoàn Bách Khoa. Phạm vi: quản lý nhân sự, kế toán, kho hàng, bán hàng.',
    },
    {
        'ma_hop_dong': 'HD-2025-003',
        'ten_hop_dong': 'Hợp đồng bán hàng - Cung cấp thiết bị công nghệ',
        'khach_hang_id': kh_minhchau.id,
        'loai_hop_dong': 'ban_hang',
        'ngay_ky': '2025-05-20',
        'ngay_hieu_luc': '2025-06-01',
        'ngay_het_han': '2025-12-31',
        'gia_tri': 480000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_dong.id,
        'trang_thai': 'hieu_luc',
        'mo_ta': 'Cung cấp thiết bị máy tính, server và hạ tầng mạng cho văn phòng mới của Công ty Minh Châu tại Quận 12.',
    },
    {
        'ma_hop_dong': 'HD-2025-004',
        'ten_hop_dong': 'Hợp đồng hợp tác chiến lược phát triển phần mềm',
        'khach_hang_id': kh_dien_luc.id,
        'loai_hop_dong': 'hop_tac',
        'ngay_ky': '2025-07-01',
        'ngay_hieu_luc': '2025-08-01',
        'ngay_het_han': '2028-07-31',
        'gia_tri': 2500000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_tuan.id,
        'trang_thai': 'hieu_luc',
        'mo_ta': 'Hợp tác chiến lược phát triển phần mềm quản lý vận hành lưới điện cho Tổng Công ty Điện lực Miền Nam. Thời hạn 3 năm, gia hạn tự động.',
    },
    {
        'ma_hop_dong': 'HD-2025-005',
        'ten_hop_dong': 'Hợp đồng dịch vụ bảo trì hệ thống thông tin',
        'khach_hang_id': kh_hoang_gia.id,
        'loai_hop_dong': 'dich_vu',
        'ngay_ky': '2025-09-15',
        'ngay_hieu_luc': '2025-10-01',
        'ngay_het_han': '2026-09-30',
        'gia_tri': 120000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_nha.id,
        'trang_thai': 'hieu_luc',
        'mo_ta': 'Dịch vụ bảo trì, vận hành và hỗ trợ kỹ thuật hệ thống thông tin cho Công ty Xây dựng Hoàng Gia.',
    },
    {
        'ma_hop_dong': 'HD-2024-015',
        'ten_hop_dong': 'Hợp đồng cung cấp giải pháp phần mềm kế toán',
        'khach_hang_id': kh_techsoft.id,
        'loai_hop_dong': 'dich_vu',
        'ngay_ky': '2024-06-01',
        'ngay_hieu_luc': '2024-07-01',
        'ngay_het_han': '2025-06-30',
        'gia_tri': 95000000,
        'don_vi_tien': 'vnd',
        'nhan_vien_phu_trach_id': nv_nha.id,
        'trang_thai': 'het_han',
        'mo_ta': 'Cung cấp và triển khai phần mềm kế toán theo chuẩn Việt Nam. Hợp đồng đã hoàn thành.',
    },
]

hop_dong_records = []
for hd_data in danh_sach_hop_dong:
    existing = env['hop_dong'].sudo().search([('ma_hop_dong', '=', hd_data['ma_hop_dong'])], limit=1)
    if existing:
        hop_dong_records.append(existing)
        print(f"  ✓ (đã có) {hd_data['ma_hop_dong']} - {hd_data['ten_hop_dong'][:45]}")
    else:
        hd = env['hop_dong'].sudo().create(hd_data)
        hop_dong_records.append(hd)
        print(f"  ✓ Tạo: {hd.ma_hop_dong} - {hd.ten_hop_dong[:45]}")

# ─────────────────────────────────────────────
# 4. VĂN BẢN
# ─────────────────────────────────────────────
print("\n[4/4] Tạo văn bản...")

# Tạo loại văn bản nếu chưa có
def lay_hoac_tao_loai_vb(ten, ma=None):
    existing = env['loai_van_ban'].sudo().search([('ten_loai', '=', ten)], limit=1)
    if existing:
        return existing.id
    rec = env['loai_van_ban'].sudo().create({'ma_loai': ma or ten[:10], 'ten_loai': ten, 'hoat_dong': True})
    return rec.id

lvb_cong_van   = lay_hoac_tao_loai_vb('Công văn', 'CV')
lvb_to_trinh   = lay_hoac_tao_loai_vb('Tờ trình', 'TT')
lvb_bao_cao    = lay_hoac_tao_loai_vb('Báo cáo', 'BC')
lvb_quyet_dinh = lay_hoac_tao_loai_vb('Quyết định', 'QD')
lvb_bien_ban   = lay_hoac_tao_loai_vb('Biên bản', 'BB')
print(f"  → Loại văn bản: Công văn(ID:{lvb_cong_van}), Tờ trình(ID:{lvb_to_trinh}), Báo cáo(ID:{lvb_bao_cao}), Quyết định(ID:{lvb_quyet_dinh}), Biên bản(ID:{lvb_bien_ban})")

# Tạo sổ công văn nếu chưa có
scv = env['so_cong_van'].sudo().search([], limit=1)
scv_id = scv.id if scv else None
if not scv_id:
    fields_scv = list(env['so_cong_van'].sudo().fields_get().keys())
    print(f"  → Sổ công văn fields: {fields_scv}")
    try:
        scv_new = env['so_cong_van'].sudo().create({
            'ma_so': 'SSCV2025',
            'ten_so': 'Sổ Công Văn 2025',
            'loai_so': 'di',
            'nam': 2025,
        })
        scv_id = scv_new.id
    except Exception as e:
        print(f"  ⚠ Không tạo được sổ công văn: {e}")

# Văn bản đi
danh_sach_vb_di = [
    {
        'so_ky_hieu': 'CV/CNTT17-2025/001',
        'trich_yeu': 'Công văn đề nghị hợp tác triển khai hệ thống ERP tại doanh nghiệp',
        'nguoi_ky': 'Lê Minh Tuấn - Giám đốc Kinh doanh',
        'noi_nhan': 'Tập đoàn Bách Khoa Việt Nam',
        'khach_hang_id': kh_bachkhoa.id,
        'loai_van_ban_id': lvb_cong_van,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_soan_thao_id': nv_nha.id,
        'trang_thai': 'da_gui',
        'ngay_van_ban': '2025-03-05',
        'ngay_gui': '2025-03-06',
        'hop_dong_id': hop_dong_records[1].id if len(hop_dong_records) > 1 else False,
        'ghi_chu': 'Văn bản đề nghị hợp tác, đã gửi và nhận phản hồi tích cực.',
    },
    {
        'so_ky_hieu': 'CV/CNTT17-2025/002',
        'trich_yeu': 'Báo cáo tiến độ triển khai dự án ERP Quý I/2025',
        'nguoi_ky': 'Nguyễn Thị Thanh Nhã - Trưởng phòng Marketing',
        'noi_nhan': 'Ban Giám Đốc Công ty',
        'loai_van_ban_id': lvb_bao_cao,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_soan_thao_id': nv_nha.id,
        'trang_thai': 'hoan_tat',
        'ngay_van_ban': '2025-04-01',
        'ghi_chu': 'Báo cáo định kỳ quý 1 năm 2025.',
    },
    {
        'so_ky_hieu': 'TT/CNTT17-2025/003',
        'trich_yeu': 'Tờ trình đề xuất nâng cấp hệ thống máy chủ và hạ tầng mạng',
        'nguoi_ky': 'Dương Ngọc Đông - Nhân viên Kỹ thuật',
        'noi_nhan': 'Giám đốc Công ty',
        'loai_van_ban_id': lvb_to_trinh,
        'do_khan': 'khan',
        'do_mat': 'binh_thuong',
        'nguoi_soan_thao_id': nv_dong.id,
        'trang_thai': 'da_duyet',
        'ngay_van_ban': '2025-05-10',
        'ghi_chu': 'Đã được Ban Giám Đốc duyệt, chuẩn bị triển khai Q3/2025.',
    },
    {
        'so_ky_hieu': 'BB/CNTT17-2025/004',
        'trich_yeu': 'Biên bản nghiệm thu hệ thống phần mềm kế toán tích hợp ERP',
        'nguoi_ky': 'Trần Văn Lâm - Nhân viên Phát triển phần mềm',
        'noi_nhan': 'Công ty TNHH Phần mềm TechSoft Việt Nam',
        'khach_hang_id': kh_techsoft.id,
        'loai_van_ban_id': lvb_bien_ban,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_soan_thao_id': nv_lam.id,
        'trang_thai': 'da_gui',
        'ngay_van_ban': '2025-06-28',
        'ngay_gui': '2025-06-30',
        'hop_dong_id': hop_dong_records[0].id,
        'ghi_chu': 'Biên bản nghiệm thu chính thức sau khi hoàn thành giai đoạn 1.',
    },
    {
        'so_ky_hieu': 'QD/CNTT17-2025/005',
        'trich_yeu': 'Quyết định bổ nhiệm Trưởng phòng Kỹ thuật - Công nghệ',
        'nguoi_ky': 'Giám đốc Công ty',
        'noi_nhan': 'Phòng Kỹ thuật - Công nghệ, Phòng Hành chính - Nhân sự',
        'loai_van_ban_id': lvb_quyet_dinh,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_soan_thao_id': nv_nha.id,
        'trang_thai': 'hoan_tat',
        'ngay_van_ban': '2025-08-01',
        'ghi_chu': 'Quyết định bổ nhiệm chính thức, có hiệu lực từ 01/08/2025.',
    },
]

vb_di_records = []
for vb_data in danh_sach_vb_di:
    existing = env['van_ban_di'].sudo().search([('so_ky_hieu', '=', vb_data['so_ky_hieu'])], limit=1)
    if existing:
        vb_di_records.append(existing)
        print(f"  ✓ (đã có) VB Đi: {vb_data['so_ky_hieu']}")
    else:
        vb = env['van_ban_di'].sudo().create(vb_data)
        vb_di_records.append(vb)
        print(f"  ✓ Tạo VB Đi: {vb.so_ky_hieu} - {vb.trich_yeu[:50]}")

# Văn bản đến
danh_sach_vb_den = [
    {
        'so_ky_hieu': 'BK/2025/147',
        'trich_yeu': 'Công văn chấp thuận hợp tác và triển khai hệ thống ERP',
        'noi_ban_hanh': 'Tập đoàn Bách Khoa Việt Nam',
        'nguoi_ky': 'Chủ tịch HĐQT Tập đoàn Bách Khoa',
        'khach_hang_id': kh_bachkhoa.id,
        'loai_van_ban_id': lvb_cong_van,
        'do_khan': 'khan',
        'do_mat': 'binh_thuong',
        'nguoi_xu_ly_id': nv_tuan.id,
        'han_xu_ly': '2025-03-20',
        'trang_thai': 'da_xu_ly',
        'ngay_den': '2025-03-08',
        'ngay_van_ban': '2025-03-07',
        'ghi_chu': 'Nhận được phản hồi tích cực từ Bách Khoa, tiến hành soạn thảo hợp đồng.',
    },
    {
        'so_ky_hieu': 'EVN/2025/088',
        'trich_yeu': 'Yêu cầu báo giá triển khai hệ thống quản lý lưới điện thông minh',
        'noi_ban_hanh': 'Tổng Công ty Điện lực Miền Nam',
        'nguoi_ky': 'Phó Tổng Giám đốc EVN SPC',
        'khach_hang_id': kh_dien_luc.id,
        'loai_van_ban_id': lvb_cong_van,
        'do_khan': 'khan',
        'do_mat': 'binh_thuong',
        'nguoi_xu_ly_id': nv_dong.id,
        'han_xu_ly': '2025-06-30',
        'trang_thai': 'da_xu_ly',
        'ngay_den': '2025-06-15',
        'ngay_van_ban': '2025-06-12',
        'ghi_chu': 'Đã xử lý - lập báo giá và nộp đúng hạn.',
    },
    {
        'so_ky_hieu': 'MC/2025/033',
        'trich_yeu': 'Thông báo điều chỉnh lịch bàn giao thiết bị và yêu cầu hỗ trợ kỹ thuật',
        'noi_ban_hanh': 'Công ty Cổ phần Thương mại Minh Châu',
        'nguoi_ky': 'Giám đốc điều hành Minh Châu Corp',
        'khach_hang_id': kh_minhchau.id,
        'loai_van_ban_id': lvb_cong_van,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_xu_ly_id': nv_lam.id,
        'han_xu_ly': '2025-08-01',
        'trang_thai': 'da_xu_ly',
        'ngay_den': '2025-07-18',
        'ngay_van_ban': '2025-07-16',
        'ghi_chu': 'Đã phối hợp điều chỉnh lịch bàn giao, khách hàng đồng ý.',
    },
    {
        'so_ky_hieu': 'TS/2025/056',
        'trich_yeu': 'Đăng ký mở rộng hợp đồng dịch vụ - Thêm module quản lý kho',
        'noi_ban_hanh': 'Công ty TNHH Phần mềm TechSoft Việt Nam',
        'nguoi_ky': 'CEO TechSoft Vietnam',
        'khach_hang_id': kh_techsoft.id,
        'loai_van_ban_id': lvb_cong_van,
        'do_khan': 'thuong',
        'do_mat': 'binh_thuong',
        'nguoi_xu_ly_id': nv_nha.id,
        'han_xu_ly': '2025-10-15',
        'trang_thai': 'dang_xu_ly',
        'ngay_den': '2025-10-01',
        'ngay_van_ban': '2025-09-28',
        'ghi_chu': 'Đang xem xét phạm vi mở rộng và lập phụ lục hợp đồng.',
    },
]

vb_den_records = []
for vb_data in danh_sach_vb_den:
    existing = env['van_ban_den'].sudo().search([('so_ky_hieu', '=', vb_data['so_ky_hieu'])], limit=1)
    if existing:
        vb_den_records.append(existing)
        print(f"  ✓ (đã có) VB Đến: {vb_data['so_ky_hieu']}")
    else:
        vb = env['van_ban_den'].sudo().create(vb_data)
        vb_den_records.append(vb)
        print(f"  ✓ Tạo VB Đến: {vb.so_ky_hieu} - {vb.trich_yeu[:50]}")

# ─────────────────────────────────────────────
# COMMIT & TỔNG KẾT
# ─────────────────────────────────────────────
env.cr.commit()

print("\n" + "=" * 60)
print("HOÀN TẤT TẠO DỮ LIỆU TEST!")
print("=" * 60)
print(f"  ✅ Nhân viên    : {len(nhan_vien_records)} bản ghi")
print(f"  ✅ Khách hàng   : {len(khach_hang_records)} bản ghi")
print(f"  ✅ Hợp đồng     : {len(hop_dong_records)} bản ghi")
print(f"  ✅ Văn bản đi   : {len(vb_di_records)} bản ghi")
print(f"  ✅ Văn bản đến  : {len(vb_den_records)} bản ghi")
print("\n  Truy cập: http://localhost:8069")
print("=" * 60)
