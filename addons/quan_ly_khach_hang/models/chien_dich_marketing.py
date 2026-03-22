# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class ChienDichMarketing(models.Model):
    _name = 'chien_dich_marketing'
    _description = 'Chiến dịch Marketing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ngay_bat_dau desc'
    _rec_name = 'ten_chien_dich'

    ma_chien_dich = fields.Char(string="Mã chiến dịch", required=True, copy=False, readonly=True, default='New')
    ten_chien_dich = fields.Char(string="Tên chiến dịch", required=True, tracking=True)
    mo_ta = fields.Html(string="Mô tả chiến dịch")

    loai_chien_dich = fields.Selection([
        ('email', 'Email Marketing'),
        ('sms', 'SMS Marketing'),
        ('su_kien', 'Sự kiện / Hội thảo'),
        ('khuyen_mai', 'Chương trình khuyến mại'),
        ('gioi_thieu', 'Chương trình giới thiệu'),
        ('content', 'Content Marketing'),
        ('khac', 'Khác'),
    ], string="Loại chiến dịch", required=True, default='email', tracking=True)

    ngay_bat_dau = fields.Date(string="Ngày bắt đầu", required=True, tracking=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", tracking=True)
    ngan_sach = fields.Float(string="Ngân sách (VNĐ)", tracking=True)
    chi_phi_thuc_te = fields.Float(string="Chi phí thực tế (VNĐ)")

    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string="Người phụ trách", ondelete='set null', tracking=True)
    
    # Đối tượng mục tiêu
    doi_tuong_muc_tieu = fields.Selection([
        ('tat_ca', 'Tất cả khách hàng'),
        ('phan_tang', 'Theo phân tầng'),
        ('vong_doi', 'Theo vòng đời'),
        ('tuy_chon', 'Tùy chọn'),
    ], string="Đối tượng mục tiêu", default='tat_ca')

    phan_tang_muc_tieu = fields.Selection([
        ('dong', 'Đồng'),
        ('bac', 'Bạc'),
        ('vang', 'Vàng'),
        ('kim_cuong', 'Kim cương'),
    ], string="Phân tầng mục tiêu")

    vong_doi_muc_tieu = fields.Selection([
        ('active', 'Đang hoạt động'),
        ('inactive', 'Không hoạt động'),
        ('churn', 'Rời bỏ'),
    ], string="Vòng đời mục tiêu")

    khach_hang_ids = fields.Many2many('khach_hang', 'chien_dich_khach_hang_rel', 'chien_dich_id', 'khach_hang_id',
                                       string="Danh sách khách hàng")

    # KPI
    so_khach_muc_tieu = fields.Integer(string="Số KH mục tiêu", compute='_compute_kpi', store=True)
    so_khach_phan_hoi = fields.Integer(string="Số KH phản hồi")
    so_co_hoi_tao = fields.Integer(string="Số cơ hội tạo mới")
    doanh_thu_tu_chien_dich = fields.Float(string="Doanh thu từ chiến dịch (VNĐ)")
    ty_le_phan_hoi = fields.Float(string="Tỷ lệ phản hồi (%)", compute='_compute_kpi', store=True)
    roi = fields.Float(string="ROI (%)", compute='_compute_kpi', store=True)

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('len_ke_hoach', 'Lên kế hoạch'),
        ('dang_chay', 'Đang chạy'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy'),
    ], string="Trạng thái", default='nhap', tracking=True)

    ghi_chu = fields.Text(string="Ghi chú")

    @api.model
    def create(self, vals):
        if vals.get('ma_chien_dich', 'New') == 'New':
            vals['ma_chien_dich'] = self.env['ir.sequence'].next_by_code('chien_dich_marketing') or 'New'
        return super().create(vals)

    @api.depends('khach_hang_ids', 'so_khach_phan_hoi', 'doanh_thu_tu_chien_dich', 'chi_phi_thuc_te')
    def _compute_kpi(self):
        for rec in self:
            rec.so_khach_muc_tieu = len(rec.khach_hang_ids)
            if rec.so_khach_muc_tieu > 0:
                rec.ty_le_phan_hoi = (rec.so_khach_phan_hoi / rec.so_khach_muc_tieu) * 100
            else:
                rec.ty_le_phan_hoi = 0
            if rec.chi_phi_thuc_te > 0:
                rec.roi = ((rec.doanh_thu_tu_chien_dich - rec.chi_phi_thuc_te) / rec.chi_phi_thuc_te) * 100
            else:
                rec.roi = 0

    def action_loc_khach_hang(self):
        """Lọc khách hàng theo đối tượng mục tiêu"""
        domain = []
        if self.doi_tuong_muc_tieu == 'phan_tang' and self.phan_tang_muc_tieu:
            domain = [('phan_tang', '=', self.phan_tang_muc_tieu)]
        elif self.doi_tuong_muc_tieu == 'vong_doi' and self.vong_doi_muc_tieu:
            domain = [('trang_thai_vong_doi', '=', self.vong_doi_muc_tieu)]

        khach_hangs = self.env['khach_hang'].search(domain)
        self.write({'khach_hang_ids': [(6, 0, khach_hangs.ids)]})

    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_chay'})

    def action_len_ke_hoach(self):
        self.write({'trang_thai': 'len_ke_hoach'})

    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh'})

    def action_huy(self):
        self.write({'trang_thai': 'huy'})
