from odoo import models, fields, api
from datetime import date

from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'chuc_vu_cap_do asc, ten asc, tuoi desc'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)

    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    
    ngay_sinh = fields.Date("Ngày sinh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'), ('nu', 'Nữ'), ('khac', 'Khác'),
    ], string="Giới tính")
    so_cmnd_cccd = fields.Char("Số CMND/CCCD")
    ngay_cap_cccd = fields.Date("Ngày cấp")
    noi_cap_cccd = fields.Char("Nơi cấp")
    que_quan = fields.Char("Quê quán")
    dia_chi_hien_tai = fields.Text("Địa chỉ hiện tại")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    trinh_do_hoc_van = fields.Selection([
        ('thpt', 'THPT'),
        ('trung_cap', 'Trung cấp'),
        ('cao_dang', 'Cao đẳng'),
        ('dai_hoc', 'Đại học'),
        ('thac_si', 'Thạc sĩ'),
        ('tien_si', 'Tiến sĩ'),
    ], string="Trình độ học vấn")
    tinh_trang_hon_nhan = fields.Selection([
        ('doc_than', 'Độc thân'),
        ('da_ket_hon', 'Đã kết hôn'),
        ('ly_hon', 'Ly hôn'),
    ], string="Tình trạng hôn nhân")
    dan_toc = fields.Char("Dân tộc")
    ton_giao = fields.Char("Tôn giáo")
    so_tai_khoan_ngan_hang = fields.Char("Số tài khoản NH")
    ten_ngan_hang = fields.Char("Ngân hàng")
    ma_so_thue = fields.Char("Mã số thuế cá nhân")
    ngay_vao_lam = fields.Date("Ngày vào làm")
    trang_thai_lam_viec = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('thu_viec', 'Thử việc'),
        ('nghi_phep', 'Nghỉ phép'),
        ('nghi_viec', 'Đã nghỉ việc'),
    ], string="Trạng thái", default='dang_lam')
    user_id = fields.Many2one('res.users', string="User liên kết", help="Liên kết user Odoo để giao activity")
    partner_id = fields.Many2one(
        'res.partner',
        string="Đối tác ERP",
        help="Đồng bộ nhân sự sang danh bạ chung để các module khác (CRM/Document) dùng chung",
        ondelete='set null',
    )
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách lịch sử công tác")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    anh = fields.Binary("Ảnh")
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap", 
        inverse_name="nhan_vien_id", 
        string = "Danh sách chứng chỉ bằng cấp")
    so_nguoi_bang_tuoi = fields.Integer(
        "Số người bằng tuổi",
        compute="_compute_so_nguoi_bang_tuoi",
        store=True,
    )
    luong_co_ban = fields.Float("Lương cơ bản")
    don_vi_hien_tai = fields.Many2one("don_vi", string="Đơn vị hiện tại", compute="_compute_don_vi_hien_tai", store=True)
    chuc_vu_cap_do = fields.Integer(string='Cấp độ chức vụ', compute='_compute_chuc_vu_cap_do', store=True)
    chuc_vu_hien_tai = fields.Many2one("chuc_vu", string="Chức vụ hiện tại", compute="_compute_chuc_vu_hien_tai", store=True)

    # Liên kết module mới
    hop_dong_lao_dong_ids = fields.One2many('hop_dong_lao_dong', 'nhan_vien_id', string="Hợp đồng lao động")
    hop_dong_lao_dong_count = fields.Integer("Số HĐLĐ", compute='_compute_hr_counts')
    nghi_phep_ids = fields.One2many('nghi_phep', 'nhan_vien_id', string="Đơn nghỉ phép")
    nghi_phep_count = fields.Integer("Số đơn phép", compute='_compute_hr_counts')
    bang_luong_ids = fields.One2many('bang_luong', 'nhan_vien_id', string="Bảng lương")
    danh_gia_kpi_ids = fields.One2many('danh_gia_kpi', 'nhan_vien_id', string="Đánh giá KPI")
    danh_gia_kpi_count = fields.Integer("Số đánh giá", compute='_compute_hr_counts')
    dao_tao_ids = fields.Many2many('dao_tao', string="Chương trình đào tạo")
    so_nghi_phep_ids = fields.One2many('so_nghi_phep', 'nhan_vien_id', string="Số ngày phép")
    
    def action_open_van_ban_di_xu_ly(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Văn bản đi xử lý",
            "res_model": "van_ban_di",
            "view_mode": "tree,form",
            "domain": [("can_bo_xu_ly_id", "=", self.id)],
        }

    def _compute_hr_counts(self):
        for rec in self:
            rec.hop_dong_lao_dong_count = len(rec.hop_dong_lao_dong_ids)
            rec.nghi_phep_count = len(rec.nghi_phep_ids)
            rec.danh_gia_kpi_count = len(rec.danh_gia_kpi_ids)

    def action_view_hop_dong_lao_dong(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Hợp đồng lao động',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id},
        }

    def action_view_nghi_phep(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đơn nghỉ phép',
            'res_model': 'nghi_phep',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id},
        }

    def action_view_danh_gia_kpi(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Đánh giá KPI',
            'res_model': 'danh_gia_kpi',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {'default_nhan_vien_id': self.id},
        }
    @api.depends("tuoi")
    def _compute_so_nguoi_bang_tuoi(self):
        for record in self:
            if not record.tuoi:
                record.so_nguoi_bang_tuoi = 0
                continue

            record_id = record.id if isinstance(record.id, int) else 0
            domain = [("tuoi", "=", record.tuoi)]
            if record_id:
                domain.append(("id", "!=", record_id))
            record.so_nguoi_bang_tuoi = self.env["nhan_vien"].search_count(domain)
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất')
    ]

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten
    
    
    
                
    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = ''.join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau
    
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        for record in self:
            if record.ngay_sinh:
                year_now = date.today().year
                record.tuoi = year_now - record.ngay_sinh.year

    @api.constrains('tuoi')
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được bé hơn 18")

    @api.depends('lich_su_cong_tac_ids.loai_chuc_vu', 'lich_su_cong_tac_ids.don_vi_id')
    def _compute_don_vi_hien_tai(self):
        for record in self:
            lich_su_chinh = record.lich_su_cong_tac_ids.filtered(lambda l: l.loai_chuc_vu == "Chính")
            if lich_su_chinh:
                record.don_vi_hien_tai = lich_su_chinh[0].don_vi_id
            else:
                record.don_vi_hien_tai = False

    @api.depends('lich_su_cong_tac_ids.loai_chuc_vu', 'lich_su_cong_tac_ids.chuc_vu_id')
    def _compute_chuc_vu_hien_tai(self):
        for record in self:
            lich_su_chinh = record.lich_su_cong_tac_ids.filtered(lambda l: l.loai_chuc_vu == "Chính")
            if lich_su_chinh:
                record.chuc_vu_hien_tai = lich_su_chinh[0].chuc_vu_id
            else:
                record.chuc_vu_hien_tai = False

    @api.depends('chuc_vu_hien_tai.cap_do')
    def _compute_chuc_vu_cap_do(self):
        for record in self:
            record.chuc_vu_cap_do = record.chuc_vu_hien_tai.cap_do if record.chuc_vu_hien_tai else 9999

    @api.model_create_multi
    def create(self, vals_list):
        records = super(NhanVien, self).create(vals_list)
        records._sync_nhan_su_data()
        return records

    def write(self, vals):
        result = super(NhanVien, self).write(vals)
        # Đồng bộ partner/user sau khi cập nhật
        self._sync_nhan_su_data()
        return result

    def _sync_nhan_su_data(self):
        """Đồng bộ nhân sự với partner/user để dùng chung toàn ERP."""
        for rec in self:
            # Tìm hoặc tạo partner theo email/sđt
            partner = rec.partner_id
            if not partner and rec.email:
                partner = rec.env['res.partner'].sudo().search([('email', '=', rec.email)], limit=1)
            if not partner and rec.so_dien_thoai:
                partner = rec.env['res.partner'].sudo().search([('phone', '=', rec.so_dien_thoai)], limit=1)
            if not partner:
                partner_vals = {
                    'name': rec.ho_va_ten or rec.ten or 'Nhân sự',
                    'email': rec.email,
                    'phone': rec.so_dien_thoai,
                }
                partner = rec.env['res.partner'].sudo().create(partner_vals)
            if partner and rec.partner_id != partner:
                rec.partner_id = partner.id
            # Liên kết user -> partner để activity tới đúng người
            if rec.user_id and partner and rec.user_id.partner_id != partner:
                rec.user_id.partner_id = partner.id
        return True
