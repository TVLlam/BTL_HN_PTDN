# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import timedelta


class KhaoSatHaiLong(models.Model):
    _name = 'khao_sat_hai_long'
    _description = 'Khảo sát mức độ hài lòng khách hàng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ngay_gui desc'
    _rec_name = 'ma_khao_sat'

    ma_khao_sat = fields.Char(string="Mã khảo sát", required=True, copy=False, readonly=True, default='New')
    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True, ondelete='cascade', tracking=True)
    don_hang_id = fields.Many2one('don_hang', string="Đơn hàng liên quan", ondelete='set null')
    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách", ondelete='set null')

    loai_khao_sat = fields.Selection([
        ('csat', 'CSAT - Hài lòng tổng thể'),
        ('nps', 'NPS - Khả năng giới thiệu'),
        ('ces', 'CES - Mức độ dễ dàng'),
    ], string="Loại khảo sát", required=True, default='csat', tracking=True)

    # Điểm đánh giá
    diem_tong_the = fields.Selection([
        ('1', '1 - Rất không hài lòng'),
        ('2', '2 - Không hài lòng'),
        ('3', '3 - Bình thường'),
        ('4', '4 - Hài lòng'),
        ('5', '5 - Rất hài lòng'),
    ], string="Đánh giá tổng thể", tracking=True)

    diem_chat_luong = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string="Chất lượng sản phẩm/dịch vụ")

    diem_giao_hang = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string="Giao hàng")

    diem_ho_tro = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string="Hỗ trợ khách hàng")

    diem_gia_ca = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
    ], string="Giá cả hợp lý")

    # NPS specific
    diem_nps = fields.Integer(string="Điểm NPS (0-10)", help="0 = Chắc chắn không, 10 = Chắc chắn có")
    nhom_nps = fields.Selection([
        ('detractor', 'Detractor (0-6)'),
        ('passive', 'Passive (7-8)'),
        ('promoter', 'Promoter (9-10)'),
    ], string="Nhóm NPS", compute='_compute_nhom_nps', store=True)

    diem_trung_binh = fields.Float(string="Điểm trung bình", compute='_compute_diem_trung_binh', store=True, digits=(3, 2))
    y_kien = fields.Text(string="Ý kiến / Góp ý")
    de_xuat_cai_tien = fields.Text(string="Đề xuất cải tiến")

    ngay_gui = fields.Date(string="Ngày gửi khảo sát", default=fields.Date.today, tracking=True)
    ngay_phan_hoi = fields.Date(string="Ngày phản hồi", tracking=True)

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_gui', 'Đã gửi'),
        ('da_phan_hoi', 'Đã phản hồi'),
        ('dong', 'Đóng'),
    ], string="Trạng thái", default='nhap', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_khao_sat', 'New') == 'New':
            vals['ma_khao_sat'] = self.env['ir.sequence'].next_by_code('khao_sat_hai_long') or 'New'
        return super().create(vals)

    @api.depends('diem_nps')
    def _compute_nhom_nps(self):
        for rec in self:
            if rec.diem_nps is False or rec.diem_nps is None:
                rec.nhom_nps = False
            elif rec.diem_nps <= 6:
                rec.nhom_nps = 'detractor'
            elif rec.diem_nps <= 8:
                rec.nhom_nps = 'passive'
            else:
                rec.nhom_nps = 'promoter'

    @api.depends('diem_tong_the', 'diem_chat_luong', 'diem_giao_hang', 'diem_ho_tro', 'diem_gia_ca')
    def _compute_diem_trung_binh(self):
        for rec in self:
            scores = []
            for f in ['diem_tong_the', 'diem_chat_luong', 'diem_giao_hang', 'diem_ho_tro', 'diem_gia_ca']:
                val = getattr(rec, f)
                if val:
                    scores.append(int(val))
            rec.diem_trung_binh = sum(scores) / len(scores) if scores else 0

    def action_gui_khao_sat(self):
        self.write({'trang_thai': 'da_gui', 'ngay_gui': fields.Date.today()})

    def action_ghi_nhan_phan_hoi(self):
        self.write({'trang_thai': 'da_phan_hoi', 'ngay_phan_hoi': fields.Date.today()})

    def action_dong(self):
        self.write({'trang_thai': 'dong'})
