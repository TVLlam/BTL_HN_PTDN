# -*- coding: utf-8 -*-
from odoo import models, fields, api


class PhieuLuanChuyen(models.Model):
    _name = 'phieu_luan_chuyen'
    _description = 'Phiếu luân chuyển văn bản'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ngay_tao desc'
    _rec_name = 'ma_phieu'

    ma_phieu = fields.Char(string="Mã phiếu", required=True, copy=False, readonly=True, default='New')

    # Liên kết văn bản
    loai_van_ban = fields.Selection([
        ('van_ban_den', 'Văn bản đến'),
        ('van_ban_di', 'Văn bản đi'),
    ], string="Loại văn bản", required=True, tracking=True)
    van_ban_den_id = fields.Many2one('van_ban_den', string="Văn bản đến", ondelete='cascade')
    van_ban_di_id = fields.Many2one('van_ban_di', string="Văn bản đi", ondelete='cascade')

    trich_yeu = fields.Char(string="Trích yếu", compute='_compute_trich_yeu', store=True)

    nguoi_chuyen_id = fields.Many2one('nhan_vien', string="Người chuyển", required=True, ondelete='restrict', tracking=True)
    don_vi_chuyen_id = fields.Many2one('don_vi', string="Đơn vị chuyển", ondelete='set null')

    # Chi tiết luân chuyển
    chi_tiet_ids = fields.One2many('phieu_luan_chuyen_chi_tiet', 'phieu_luan_chuyen_id', string="Chi tiết luân chuyển")

    ngay_tao = fields.Datetime(string="Ngày tạo", default=fields.Datetime.now, readonly=True)
    han_xu_ly = fields.Date(string="Hạn xử lý", tracking=True)
    y_kien_chi_dao = fields.Text(string="Ý kiến chỉ đạo")

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('dang_luan_chuyen', 'Đang luân chuyển'),
        ('hoan_tat', 'Hoàn tất'),
        ('thu_hoi', 'Thu hồi'),
    ], string="Trạng thái", default='nhap', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('ma_phieu', 'New') == 'New':
            vals['ma_phieu'] = self.env['ir.sequence'].next_by_code('phieu_luan_chuyen') or 'New'
        return super().create(vals)

    @api.depends('van_ban_den_id', 'van_ban_di_id', 'loai_van_ban')
    def _compute_trich_yeu(self):
        for rec in self:
            if rec.loai_van_ban == 'van_ban_den' and rec.van_ban_den_id:
                rec.trich_yeu = rec.van_ban_den_id.trich_yeu
            elif rec.loai_van_ban == 'van_ban_di' and rec.van_ban_di_id:
                rec.trich_yeu = rec.van_ban_di_id.trich_yeu
            else:
                rec.trich_yeu = ''

    def action_bat_dau_luan_chuyen(self):
        self.write({'trang_thai': 'dang_luan_chuyen'})
        # Tạo activity cho người nhận đầu tiên
        for chi_tiet in self.chi_tiet_ids.filtered(lambda c: c.thu_tu == 1):
            if chi_tiet.nguoi_nhan_id:
                user = self.env['res.users'].search([('id', '!=', 0)], limit=1)
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=self.han_xu_ly,
                    summary='Nhận văn bản luân chuyển: %s' % self.ma_phieu,
                    user_id=user.id,
                )

    def action_hoan_tat(self):
        self.write({'trang_thai': 'hoan_tat'})

    def action_thu_hoi(self):
        self.write({'trang_thai': 'thu_hoi'})


class PhieuLuanChuyenChiTiet(models.Model):
    _name = 'phieu_luan_chuyen_chi_tiet'
    _description = 'Chi tiết luân chuyển'
    _order = 'thu_tu'
    _rec_name = 'nguoi_nhan_id'

    phieu_luan_chuyen_id = fields.Many2one('phieu_luan_chuyen', string="Phiếu luân chuyển",
                                             required=True, ondelete='cascade')
    thu_tu = fields.Integer(string="Thứ tự", required=True, default=1)
    nguoi_nhan_id = fields.Many2one('nhan_vien', string="Người nhận", required=True, ondelete='restrict')
    don_vi_nhan_id = fields.Many2one('don_vi', string="Đơn vị nhận", ondelete='set null')

    ngay_nhan = fields.Datetime(string="Ngày nhận")
    ngay_chuyen_tiep = fields.Datetime(string="Ngày chuyển tiếp")
    y_kien = fields.Text(string="Ý kiến xử lý")

    trang_thai = fields.Selection([
        ('cho_nhan', 'Chờ nhận'),
        ('da_nhan', 'Đã nhận'),
        ('da_xu_ly', 'Đã xử lý'),
        ('chuyen_tiep', 'Chuyển tiếp'),
    ], string="Trạng thái", default='cho_nhan')

    def action_nhan_van_ban(self):
        self.write({
            'trang_thai': 'da_nhan',
            'ngay_nhan': fields.Datetime.now(),
        })

    def action_xu_ly_xong(self):
        self.write({'trang_thai': 'da_xu_ly'})

    def action_chuyen_tiep(self):
        self.write({
            'trang_thai': 'chuyen_tiep',
            'ngay_chuyen_tiep': fields.Datetime.now(),
        })
        # Chuyển tiếp cho người tiếp theo
        next_step = self.env['phieu_luan_chuyen_chi_tiet'].search([
            ('phieu_luan_chuyen_id', '=', self.phieu_luan_chuyen_id.id),
            ('thu_tu', '>', self.thu_tu),
        ], order='thu_tu', limit=1)
        if not next_step:
            self.phieu_luan_chuyen_id.action_hoan_tat()
