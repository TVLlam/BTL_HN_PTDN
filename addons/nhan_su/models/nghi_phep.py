# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NghiPhep(models.Model):
    _name = 'nghi_phep'
    _description = 'Quản lý nghỉ phép'
    _rec_name = 'ma_don'
    _order = 'ngay_bat_dau desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_don = fields.Char("Mã đơn", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    don_vi_id = fields.Many2one('don_vi', string="Phòng ban", related='nhan_vien_id.don_vi_hien_tai', store=True)

    loai_nghi = fields.Selection([
        ('phep_nam', 'Phép năm'),
        ('om_dau', 'Ốm đau'),
        ('thai_san', 'Thai sản'),
        ('cuoi', 'Nghỉ cưới'),
        ('tang', 'Nghỉ tang'),
        ('viec_rieng', 'Việc riêng (không lương)'),
        ('khac', 'Khác'),
    ], string="Loại nghỉ", required=True, tracking=True)

    ngay_bat_dau = fields.Date("Từ ngày", required=True, tracking=True)
    ngay_ket_thuc = fields.Date("Đến ngày", required=True, tracking=True)
    so_ngay = fields.Float("Số ngày nghỉ", compute='_compute_so_ngay', store=True)

    ly_do = fields.Text("Lý do", required=True)
    nguoi_duyet_id = fields.Many2one('nhan_vien', string="Người duyệt")

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='nhap', tracking=True)

    ly_do_tu_choi = fields.Text("Lý do từ chối")
    file_dinh_kem = fields.Binary("File đính kèm")
    file_dinh_kem_name = fields.Char("Tên file")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ma_don', 'New') == 'New':
                vals['ma_don'] = self.env['ir.sequence'].next_by_code('nghi_phep') or 'New'
        return super().create(vals_list)

    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_so_ngay(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc:
                delta = (rec.ngay_ket_thuc - rec.ngay_bat_dau).days + 1
                rec.so_ngay = max(delta, 0)
            else:
                rec.so_ngay = 0

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc and rec.ngay_ket_thuc < rec.ngay_bat_dau:
                raise ValidationError("Ngày kết thúc phải sau ngày bắt đầu!")

    def action_gui_duyet(self):
        self.write({'trang_thai': 'cho_duyet'})

    def action_duyet(self):
        self.write({'trang_thai': 'duyet'})
        self._send_leave_notification('duyet')

    def action_tu_choi(self):
        self.write({'trang_thai': 'tu_choi'})
        self._send_leave_notification('tu_choi')

    def _send_leave_notification(self, action):
        """Gửi email thông báo duyệt / từ chối nghỉ phép"""
        service = self.env['email.notification.service']
        for rec in self:
            email = rec.nhan_vien_id.email
            if not email:
                continue
            if action == 'duyet':
                title = 'Đơn nghỉ phép đã được DUYỆT'
                greeting = f'Xin chào {rec.nhan_vien_id.ho_va_ten},<br>Đơn nghỉ phép của bạn đã được <b style="color:green;">duyệt</b>.'
            else:
                title = 'Đơn nghỉ phép bị TỪ CHỐI'
                greeting = f'Xin chào {rec.nhan_vien_id.ho_va_ten},<br>Đơn nghỉ phép của bạn đã bị <b style="color:red;">từ chối</b>.'
            lines = [
                ('Mã đơn', rec.ma_don),
                ('Loại nghỉ', dict(rec._fields['loai_nghi'].selection).get(rec.loai_nghi, '')),
                ('Từ ngày', str(rec.ngay_bat_dau)),
                ('Đến ngày', str(rec.ngay_ket_thuc)),
                ('Số ngày', str(rec.so_ngay)),
            ]
            if action == 'tu_choi' and rec.ly_do_tu_choi:
                lines.append(('Lý do từ chối', rec.ly_do_tu_choi))
            body = service._build_email_html(title, greeting, lines)
            ok, msg = service.send_email(email, title, body, from_name='Hệ thống Nhân sự')
            rec.message_post(body=msg)

    def action_huy(self):
        self.write({'trang_thai': 'huy'})


class SoNghiPhep(models.Model):
    _name = 'so_nghi_phep'
    _description = 'Số ngày phép còn lại theo năm'
    _rec_name = 'nhan_vien_id'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)
    tong_phep_nam = fields.Float("Tổng phép năm", default=12)
    da_nghi = fields.Float("Đã nghỉ", compute='_compute_da_nghi', store=True)
    con_lai = fields.Float("Còn lại", compute='_compute_con_lai', store=True)

    @api.depends('nhan_vien_id', 'nam', 'tong_phep_nam')
    def _compute_da_nghi(self):
        for rec in self:
            nghi = self.env['nghi_phep'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('trang_thai', '=', 'duyet'),
                ('loai_nghi', '=', 'phep_nam'),
                ('ngay_bat_dau', '>=', f'{rec.nam}-01-01'),
                ('ngay_bat_dau', '<=', f'{rec.nam}-12-31'),
            ])
            rec.da_nghi = sum(nghi.mapped('so_ngay'))

    @api.depends('tong_phep_nam', 'da_nghi')
    def _compute_con_lai(self):
        for rec in self:
            rec.con_lai = rec.tong_phep_nam - rec.da_nghi

    _sql_constraints = [
        ('nhanvien_nam_unique', 'unique(nhan_vien_id, nam)', 'Mỗi nhân viên chỉ có 1 bản ghi phép/năm!')
    ]
