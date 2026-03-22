# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DanhGiaKPI(models.Model):
    _name = 'danh_gia_kpi'
    _description = 'Đánh giá KPI nhân viên'
    _rec_name = 'ma_danh_gia'
    _order = 'nam desc, quy desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_danh_gia = fields.Char("Mã đánh giá", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    don_vi_id = fields.Many2one('don_vi', string="Phòng ban", related='nhan_vien_id.don_vi_hien_tai', store=True)
    nguoi_danh_gia_id = fields.Many2one('nhan_vien', string="Người đánh giá")

    ky_danh_gia = fields.Selection([
        ('thang', 'Hàng tháng'),
        ('quy', 'Hàng quý'),
        ('nam', 'Hàng năm'),
    ], string="Kỳ đánh giá", required=True, default='quy')
    quy = fields.Selection([
        ('1', 'Quý 1'), ('2', 'Quý 2'), ('3', 'Quý 3'), ('4', 'Quý 4'),
    ], string="Quý")
    thang = fields.Selection([
        ('1', 'T1'), ('2', 'T2'), ('3', 'T3'), ('4', 'T4'),
        ('5', 'T5'), ('6', 'T6'), ('7', 'T7'), ('8', 'T8'),
        ('9', 'T9'), ('10', 'T10'), ('11', 'T11'), ('12', 'T12'),
    ], string="Tháng")
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)

    # Tiêu chí đánh giá (thang 1-5)
    hoan_thanh_cong_viec = fields.Selection([
        ('1', '1 - Yếu'), ('2', '2 - Trung bình'), ('3', '3 - Khá'),
        ('4', '4 - Tốt'), ('5', '5 - Xuất sắc'),
    ], string="Hoàn thành công việc", required=True)
    chat_luong = fields.Selection([
        ('1', '1 - Yếu'), ('2', '2 - Trung bình'), ('3', '3 - Khá'),
        ('4', '4 - Tốt'), ('5', '5 - Xuất sắc'),
    ], string="Chất lượng công việc", required=True)
    sang_tao = fields.Selection([
        ('1', '1 - Yếu'), ('2', '2 - Trung bình'), ('3', '3 - Khá'),
        ('4', '4 - Tốt'), ('5', '5 - Xuất sắc'),
    ], string="Sáng tạo & Cải tiến", required=True)
    lam_viec_nhom = fields.Selection([
        ('1', '1 - Yếu'), ('2', '2 - Trung bình'), ('3', '3 - Khá'),
        ('4', '4 - Tốt'), ('5', '5 - Xuất sắc'),
    ], string="Làm việc nhóm", required=True)
    ky_luat = fields.Selection([
        ('1', '1 - Yếu'), ('2', '2 - Trung bình'), ('3', '3 - Khá'),
        ('4', '4 - Tốt'), ('5', '5 - Xuất sắc'),
    ], string="Kỷ luật & Thái độ", required=True)

    diem_trung_binh = fields.Float("Điểm trung bình", compute='_compute_diem', store=True)
    xep_loai = fields.Selection([
        ('xuat_sac', 'Xuất sắc'),
        ('tot', 'Tốt'),
        ('kha', 'Khá'),
        ('trung_binh', 'Trung bình'),
        ('yeu', 'Yếu'),
    ], string="Xếp loại", compute='_compute_diem', store=True)

    nhan_xet_nhan_vien = fields.Text("Nhân viên tự nhận xét")
    nhan_xet_quan_ly = fields.Text("Nhận xét của quản lý")
    muc_tieu_ky_toi = fields.Text("Mục tiêu kỳ tới")

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
    ], string="Trạng thái", default='nhap', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ma_danh_gia', 'New') == 'New':
                vals['ma_danh_gia'] = self.env['ir.sequence'].next_by_code('danh_gia_kpi') or 'New'
        return super().create(vals_list)

    @api.depends('hoan_thanh_cong_viec', 'chat_luong', 'sang_tao', 'lam_viec_nhom', 'ky_luat')
    def _compute_diem(self):
        for rec in self:
            vals = [rec.hoan_thanh_cong_viec, rec.chat_luong, rec.sang_tao, rec.lam_viec_nhom, rec.ky_luat]
            diem_list = [int(v) for v in vals if v]
            if diem_list:
                rec.diem_trung_binh = sum(diem_list) / len(diem_list)
            else:
                rec.diem_trung_binh = 0

            d = rec.diem_trung_binh
            if d >= 4.5:
                rec.xep_loai = 'xuat_sac'
            elif d >= 3.5:
                rec.xep_loai = 'tot'
            elif d >= 2.5:
                rec.xep_loai = 'kha'
            elif d >= 1.5:
                rec.xep_loai = 'trung_binh'
            else:
                rec.xep_loai = 'yeu'

    def action_gui_duyet(self):
        self.write({'trang_thai': 'cho_duyet'})

    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh'})
