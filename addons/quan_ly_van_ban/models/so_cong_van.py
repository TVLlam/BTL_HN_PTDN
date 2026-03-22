# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SoCongVan(models.Model):
    _name = 'so_cong_van'
    _description = 'Sổ công văn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'nam desc, loai_so'
    _rec_name = 'ten_so'

    ma_so = fields.Char(string="Mã sổ", required=True, copy=False, readonly=True, default='New')
    ten_so = fields.Char(string="Tên sổ", required=True, tracking=True)
    loai_so = fields.Selection([
        ('den', 'Sổ công văn đến'),
        ('di', 'Sổ công văn đi'),
    ], string="Loại sổ", required=True, tracking=True)

    nam = fields.Integer(string="Năm", required=True, default=lambda self: fields.Date.today().year, tracking=True)
    don_vi_id = fields.Many2one('don_vi', string="Đơn vị/Phòng ban", ondelete='set null')
    nguoi_quan_ly_id = fields.Many2one('nhan_vien', string="Người quản lý sổ", ondelete='set null', tracking=True)

    mo_ta = fields.Text(string="Mô tả")
    trang_thai = fields.Selection([
        ('mo', 'Đang mở'),
        ('khoa', 'Đã khóa'),
    ], string="Trạng thái", default='mo', tracking=True)

    # Thống kê
    so_luong_van_ban = fields.Integer(string="Số lượng văn bản", compute='_compute_thong_ke', store=True)
    van_ban_den_ids = fields.One2many('van_ban_den', 'so_cong_van_id', string="Văn bản đến")
    van_ban_di_ids = fields.One2many('van_ban_di', 'so_cong_van_id', string="Văn bản đi")

    _sql_constraints = [
        ('unique_so_nam_loai', 'unique(nam, loai_so, don_vi_id)', 'Mỗi đơn vị chỉ có một sổ công văn cho mỗi loại trong một năm!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('ma_so', 'New') == 'New':
            vals['ma_so'] = self.env['ir.sequence'].next_by_code('so_cong_van') or 'New'
        return super().create(vals)

    @api.depends('van_ban_den_ids', 'van_ban_di_ids')
    def _compute_thong_ke(self):
        for rec in self:
            if rec.loai_so == 'den':
                rec.so_luong_van_ban = len(rec.van_ban_den_ids)
            else:
                rec.so_luong_van_ban = len(rec.van_ban_di_ids)

    def action_khoa_so(self):
        self.write({'trang_thai': 'khoa'})

    def action_mo_so(self):
        self.write({'trang_thai': 'mo'})
