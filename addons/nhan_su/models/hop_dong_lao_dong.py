# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class HopDongLaoDong(models.Model):
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp đồng lao động'
    _rec_name = 'ma_hop_dong'
    _order = 'ngay_bat_dau desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_hop_dong = fields.Char("Mã hợp đồng", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('xac_dinh_thoi_han', 'Xác định thời hạn'),
        ('khong_thoi_han', 'Không thời hạn'),
        ('thoi_vu', 'Thời vụ / Theo công việc'),
    ], string="Loại hợp đồng", required=True, tracking=True)
    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True, tracking=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc", tracking=True)
    thoi_han_thang = fields.Integer("Thời hạn (tháng)", compute='_compute_thoi_han', store=True)

    luong_co_ban = fields.Float("Lương cơ bản", required=True, tracking=True)
    phu_cap_an = fields.Float("Phụ cấp ăn", default=0)
    phu_cap_di_lai = fields.Float("Phụ cấp đi lại", default=0)
    phu_cap_dien_thoai = fields.Float("Phụ cấp điện thoại", default=0)
    phu_cap_khac = fields.Float("Phụ cấp khác", default=0)
    tong_thu_nhap = fields.Float("Tổng thu nhập", compute='_compute_tong_thu_nhap', store=True)

    chuc_danh = fields.Char("Chức danh")
    don_vi_id = fields.Many2one('don_vi', string="Đơn vị/Phòng ban")
    dia_diem_lam_viec = fields.Char("Địa điểm làm việc")

    trang_thai = fields.Selection([
        ('moi', 'Mới tạo'),
        ('hieu_luc', 'Đang hiệu lực'),
        ('sap_het_han', 'Sắp hết hạn'),
        ('het_han', 'Hết hạn'),
        ('cham_dut', 'Chấm dứt'),
    ], string="Trạng thái", default='moi', tracking=True)

    ly_do_cham_dut = fields.Text("Lý do chấm dứt")
    ngay_cham_dut = fields.Date("Ngày chấm dứt")
    file_hop_dong = fields.Binary("File hợp đồng")
    file_hop_dong_name = fields.Char("Tên file")
    ghi_chu = fields.Text("Ghi chú")

    _sql_constraints = [
        ('ma_hop_dong_unique', 'unique(ma_hop_dong)', 'Mã hợp đồng phải là duy nhất!')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ma_hop_dong', 'New') == 'New':
                vals['ma_hop_dong'] = self.env['ir.sequence'].next_by_code('hop_dong_lao_dong') or 'New'
        return super().create(vals_list)

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_thoi_han(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc:
                delta = relativedelta(rec.ngay_ket_thuc, rec.ngay_bat_dau)
                rec.thoi_han_thang = delta.years * 12 + delta.months
            else:
                rec.thoi_han_thang = 0

    @api.depends('luong_co_ban', 'phu_cap_an', 'phu_cap_di_lai', 'phu_cap_dien_thoai', 'phu_cap_khac')
    def _compute_tong_thu_nhap(self):
        for rec in self:
            rec.tong_thu_nhap = rec.luong_co_ban + rec.phu_cap_an + rec.phu_cap_di_lai + rec.phu_cap_dien_thoai + rec.phu_cap_khac

    def action_kich_hoat(self):
        self.write({'trang_thai': 'hieu_luc'})

    def action_cham_dut(self):
        self.write({
            'trang_thai': 'cham_dut',
            'ngay_cham_dut': fields.Date.today(),
        })

    @api.model
    def _cron_cap_nhat_trang_thai(self):
        """Cron job: tự động cập nhật trạng thái hợp đồng."""
        today = fields.Date.today()
        warning_date = today + relativedelta(months=1)

        # Hết hạn
        self.search([
            ('trang_thai', 'in', ['hieu_luc', 'sap_het_han']),
            ('ngay_ket_thuc', '<', today),
        ]).write({'trang_thai': 'het_han'})

        # Sắp hết hạn (trong vòng 1 tháng)
        self.search([
            ('trang_thai', '=', 'hieu_luc'),
            ('ngay_ket_thuc', '>=', today),
            ('ngay_ket_thuc', '<=', warning_date),
        ]).write({'trang_thai': 'sap_het_han'})
