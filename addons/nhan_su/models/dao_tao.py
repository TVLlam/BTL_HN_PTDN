# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DaoTao(models.Model):
    _name = 'dao_tao'
    _description = 'Chương trình đào tạo'
    _rec_name = 'ten_chuong_trinh'
    _order = 'ngay_bat_dau desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_dao_tao = fields.Char("Mã chương trình", required=True, copy=False, readonly=True, default='New')
    ten_chuong_trinh = fields.Char("Tên chương trình", required=True)
    loai_dao_tao = fields.Selection([
        ('noi_bo', 'Đào tạo nội bộ'),
        ('ben_ngoai', 'Đào tạo bên ngoài'),
        ('online', 'Đào tạo trực tuyến'),
        ('hoi_thao', 'Hội thảo / Workshop'),
    ], string="Loại đào tạo", required=True)

    ngay_bat_dau = fields.Date("Ngày bắt đầu", required=True)
    ngay_ket_thuc = fields.Date("Ngày kết thúc")
    so_gio = fields.Float("Số giờ đào tạo")
    dia_diem = fields.Char("Địa điểm")
    giang_vien = fields.Char("Giảng viên / Đơn vị đào tạo")

    nhan_vien_ids = fields.Many2many('nhan_vien', string="Nhân viên tham gia")
    so_luong_tham_gia = fields.Integer("Số lượng tham gia", compute='_compute_so_luong', store=True)

    chi_phi = fields.Float("Chi phí (VNĐ)")
    mo_ta = fields.Html("Nội dung đào tạo")
    ket_qua = fields.Text("Kết quả / Đánh giá")
    file_tai_lieu = fields.Binary("Tài liệu đào tạo")
    file_tai_lieu_name = fields.Char("Tên file")

    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('dang_dien_ra', 'Đang diễn ra'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='du_kien', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ma_dao_tao', 'New') == 'New':
                vals['ma_dao_tao'] = self.env['ir.sequence'].next_by_code('dao_tao') or 'New'
        return super().create(vals_list)

    @api.depends('nhan_vien_ids')
    def _compute_so_luong(self):
        for rec in self:
            rec.so_luong_tham_gia = len(rec.nhan_vien_ids)

    def action_bat_dau(self):
        self.write({'trang_thai': 'dang_dien_ra'})

    def action_hoan_thanh(self):
        self.write({'trang_thai': 'hoan_thanh'})

    def action_huy(self):
        self.write({'trang_thai': 'huy'})
