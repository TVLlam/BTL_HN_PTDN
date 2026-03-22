# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date


class LuuTruVanBan(models.Model):
    _name = 'luu_tru_van_ban'
    _description = 'Lưu trữ và thu hồi văn bản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ngay_luu_tru desc'
    _rec_name = 'ma_luu_tru'

    ma_luu_tru = fields.Char(string="Mã lưu trữ", required=True, copy=False, readonly=True, default='New')

    loai_van_ban = fields.Selection([
        ('van_ban_den', 'Văn bản đến'),
        ('van_ban_di', 'Văn bản đi'),
    ], string="Loại văn bản", required=True)
    van_ban_den_id = fields.Many2one('van_ban_den', string="Văn bản đến", ondelete='restrict')
    van_ban_di_id = fields.Many2one('van_ban_di', string="Văn bản đi", ondelete='restrict')

    so_ky_hieu = fields.Char(string="Số/Ký hiệu", compute='_compute_thong_tin_vb', store=True)
    trich_yeu = fields.Char(string="Trích yếu", compute='_compute_thong_tin_vb', store=True)

    nguoi_luu_tru_id = fields.Many2one('nhan_vien', string="Người lưu trữ", required=True, ondelete='restrict', tracking=True)
    vi_tri_luu_tru = fields.Char(string="Vị trí lưu trữ", help="Tủ/Kệ/Ngăn/Hộp", tracking=True)
    thoi_han_luu_tru = fields.Selection([
        ('5', '5 năm'),
        ('10', '10 năm'),
        ('20', '20 năm'),
        ('vinh_vien', 'Vĩnh viễn'),
    ], string="Thời hạn lưu trữ", default='10', required=True, tracking=True)

    ngay_luu_tru = fields.Date(string="Ngày lưu trữ", default=fields.Date.today, required=True, tracking=True)
    ngay_het_han = fields.Date(string="Ngày hết hạn lưu trữ", compute='_compute_ngay_het_han', store=True)

    trang_thai = fields.Selection([
        ('luu_tru', 'Đang lưu trữ'),
        ('cho_huy', 'Chờ hủy'),
        ('da_huy', 'Đã hủy'),
        ('thu_hoi', 'Đã thu hồi'),
    ], string="Trạng thái", default='luu_tru', tracking=True)

    ghi_chu = fields.Text(string="Ghi chú")
    ly_do_thu_hoi = fields.Text(string="Lý do thu hồi")
    nguoi_thu_hoi_id = fields.Many2one('nhan_vien', string="Người thu hồi", ondelete='set null')
    ngay_thu_hoi = fields.Date(string="Ngày thu hồi")

    ly_do_huy = fields.Text(string="Lý do hủy")
    nguoi_duyet_huy_id = fields.Many2one('nhan_vien', string="Người duyệt hủy", ondelete='set null')
    ngay_huy = fields.Date(string="Ngày hủy")

    @api.model
    def create(self, vals):
        if vals.get('ma_luu_tru', 'New') == 'New':
            vals['ma_luu_tru'] = self.env['ir.sequence'].next_by_code('luu_tru_van_ban') or 'New'
        return super().create(vals)

    @api.depends('van_ban_den_id', 'van_ban_di_id', 'loai_van_ban')
    def _compute_thong_tin_vb(self):
        for rec in self:
            if rec.loai_van_ban == 'van_ban_den' and rec.van_ban_den_id:
                rec.so_ky_hieu = rec.van_ban_den_id.so_ky_hieu
                rec.trich_yeu = rec.van_ban_den_id.trich_yeu
            elif rec.loai_van_ban == 'van_ban_di' and rec.van_ban_di_id:
                rec.so_ky_hieu = rec.van_ban_di_id.so_ky_hieu
                rec.trich_yeu = rec.van_ban_di_id.trich_yeu
            else:
                rec.so_ky_hieu = ''
                rec.trich_yeu = ''

    @api.depends('ngay_luu_tru', 'thoi_han_luu_tru')
    def _compute_ngay_het_han(self):
        for rec in self:
            if rec.ngay_luu_tru and rec.thoi_han_luu_tru != 'vinh_vien':
                years = int(rec.thoi_han_luu_tru) if rec.thoi_han_luu_tru else 10
                rec.ngay_het_han = rec.ngay_luu_tru.replace(year=rec.ngay_luu_tru.year + years)
            else:
                rec.ngay_het_han = False

    def action_de_xuat_huy(self):
        self.write({'trang_thai': 'cho_huy'})

    def action_duyet_huy(self):
        self.write({
            'trang_thai': 'da_huy',
            'ngay_huy': fields.Date.today(),
        })

    def action_thu_hoi(self):
        self.write({
            'trang_thai': 'thu_hoi',
            'ngay_thu_hoi': fields.Date.today(),
        })

    def action_luu_tru_lai(self):
        """Lưu trữ lại sau khi thu hồi"""
        self.write({
            'trang_thai': 'luu_tru',
            'ly_do_thu_hoi': False,
            'nguoi_thu_hoi_id': False,
            'ngay_thu_hoi': False,
        })

    @api.model
    def _cron_canh_bao_het_han(self):
        """Cảnh báo văn bản sắp hết hạn lưu trữ (trong 30 ngày)"""
        from datetime import timedelta
        ngay_canh_bao = date.today() + timedelta(days=30)
        sap_het_han = self.search([
            ('trang_thai', '=', 'luu_tru'),
            ('ngay_het_han', '!=', False),
            ('ngay_het_han', '<=', ngay_canh_bao),
            ('ngay_het_han', '>=', date.today()),
        ])
        for rec in sap_het_han:
            rec.message_post(
                body='⚠️ Văn bản %s sắp hết hạn lưu trữ vào ngày %s' % (rec.so_ky_hieu, rec.ngay_het_han),
                subject='Cảnh báo hết hạn lưu trữ',
            )
