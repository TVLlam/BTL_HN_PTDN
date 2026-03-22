# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương hàng tháng'
    _rec_name = 'ma_bang_luong'
    _order = 'nam desc, thang desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ma_bang_luong = fields.Char("Mã bảng lương", required=True, copy=False, readonly=True, default='New')
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    don_vi_id = fields.Many2one('don_vi', string="Phòng ban", related='nhan_vien_id.don_vi_hien_tai', store=True)

    thang = fields.Selection([
        ('1', 'Tháng 1'), ('2', 'Tháng 2'), ('3', 'Tháng 3'),
        ('4', 'Tháng 4'), ('5', 'Tháng 5'), ('6', 'Tháng 6'),
        ('7', 'Tháng 7'), ('8', 'Tháng 8'), ('9', 'Tháng 9'),
        ('10', 'Tháng 10'), ('11', 'Tháng 11'), ('12', 'Tháng 12'),
    ], string="Tháng", required=True)
    nam = fields.Integer("Năm", required=True, default=lambda self: fields.Date.today().year)

    # Thu nhập
    luong_co_ban = fields.Float("Lương cơ bản")
    ngay_cong_thuc_te = fields.Float("Ngày công thực tế", default=22)
    ngay_cong_chuan = fields.Float("Ngày công chuẩn", default=22)
    luong_theo_ngay_cong = fields.Float("Lương theo ngày công", compute='_compute_luong', store=True)
    phu_cap_an = fields.Float("Phụ cấp ăn")
    phu_cap_di_lai = fields.Float("Phụ cấp đi lại")
    phu_cap_khac = fields.Float("Phụ cấp khác")
    thuong = fields.Float("Thưởng")
    lam_them = fields.Float("Làm thêm giờ (VNĐ)")
    tong_thu_nhap = fields.Float("Tổng thu nhập", compute='_compute_luong', store=True)

    # Khấu trừ
    bhxh_nld = fields.Float("BHXH (8%)", compute='_compute_bao_hiem', store=True)
    bhyt_nld = fields.Float("BHYT (1.5%)", compute='_compute_bao_hiem', store=True)
    bhtn_nld = fields.Float("BHTN (1%)", compute='_compute_bao_hiem', store=True)
    tong_bao_hiem_nld = fields.Float("Tổng BH người LĐ", compute='_compute_bao_hiem', store=True)

    giam_tru_ban_than = fields.Float("Giảm trừ bản thân", default=11000000)
    so_nguoi_phu_thuoc = fields.Integer("Số người phụ thuộc", default=0)
    giam_tru_phu_thuoc = fields.Float("Giảm trừ phụ thuộc", compute='_compute_thue', store=True)
    thu_nhap_chiu_thue = fields.Float("Thu nhập chịu thuế", compute='_compute_thue', store=True)
    thue_tncn = fields.Float("Thuế TNCN", compute='_compute_thue', store=True)

    khau_tru_khac = fields.Float("Khấu trừ khác")
    tong_khau_tru = fields.Float("Tổng khấu trừ", compute='_compute_luong', store=True)

    # Thực lĩnh
    thuc_linh = fields.Float("Thực lĩnh", compute='_compute_luong', store=True)

    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('xac_nhan', 'Đã xác nhận'),
        ('da_chi', 'Đã chi trả'),
    ], string="Trạng thái", default='nhap', tracking=True)

    ghi_chu = fields.Text("Ghi chú")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ma_bang_luong', 'New') == 'New':
                vals['ma_bang_luong'] = self.env['ir.sequence'].next_by_code('bang_luong') or 'New'
        return super().create(vals_list)

    @api.depends('luong_co_ban')
    def _compute_bao_hiem(self):
        for rec in self:
            rec.bhxh_nld = rec.luong_co_ban * 0.08
            rec.bhyt_nld = rec.luong_co_ban * 0.015
            rec.bhtn_nld = rec.luong_co_ban * 0.01
            rec.tong_bao_hiem_nld = rec.bhxh_nld + rec.bhyt_nld + rec.bhtn_nld

    @api.depends('tong_thu_nhap', 'tong_bao_hiem_nld', 'giam_tru_ban_than', 'so_nguoi_phu_thuoc')
    def _compute_thue(self):
        for rec in self:
            rec.giam_tru_phu_thuoc = rec.so_nguoi_phu_thuoc * 4400000
            thu_nhap_tinh_thue = rec.tong_thu_nhap - rec.tong_bao_hiem_nld - rec.giam_tru_ban_than - rec.giam_tru_phu_thuoc
            rec.thu_nhap_chiu_thue = max(thu_nhap_tinh_thue, 0)
            rec.thue_tncn = rec._tinh_thue_luy_tien(rec.thu_nhap_chiu_thue)

    @api.depends(
        'luong_co_ban', 'ngay_cong_thuc_te', 'ngay_cong_chuan',
        'phu_cap_an', 'phu_cap_di_lai', 'phu_cap_khac',
        'thuong', 'lam_them',
        'tong_bao_hiem_nld', 'thue_tncn', 'khau_tru_khac',
    )
    def _compute_luong(self):
        for rec in self:
            if rec.ngay_cong_chuan > 0:
                rec.luong_theo_ngay_cong = rec.luong_co_ban * rec.ngay_cong_thuc_te / rec.ngay_cong_chuan
            else:
                rec.luong_theo_ngay_cong = 0
            rec.tong_thu_nhap = (
                rec.luong_theo_ngay_cong + rec.phu_cap_an + rec.phu_cap_di_lai
                + rec.phu_cap_khac + rec.thuong + rec.lam_them
            )
            rec.tong_khau_tru = rec.tong_bao_hiem_nld + rec.thue_tncn + rec.khau_tru_khac
            rec.thuc_linh = rec.tong_thu_nhap - rec.tong_khau_tru

    @staticmethod
    def _tinh_thue_luy_tien(thu_nhap):
        """Tính thuế TNCN theo biểu lũy tiến từng phần."""
        bac = [
            (5000000, 0.05),
            (5000000, 0.10),
            (8000000, 0.15),
            (14000000, 0.20),
            (20000000, 0.25),
            (28000000, 0.30),
            (float('inf'), 0.35),
        ]
        thue = 0.0
        con_lai = thu_nhap
        for muc, ty_le in bac:
            if con_lai <= 0:
                break
            tinh = min(con_lai, muc)
            thue += tinh * ty_le
            con_lai -= tinh
        return thue

    def action_xac_nhan(self):
        self.write({'trang_thai': 'xac_nhan'})

    def action_chi_tra(self):
        self.write({'trang_thai': 'da_chi'})
        self._send_salary_notification()

    def _send_salary_notification(self):
        """Gửi email thông báo lương đã chi trả"""
        service = self.env['email.notification.service']
        for rec in self:
            email = rec.nhan_vien_id.email
            if not email:
                continue
            title = f'Thông báo lương tháng {rec.thang}/{rec.nam}'
            greeting = f'Xin chào {rec.nhan_vien_id.ho_va_ten},<br>Lương của bạn đã được <b style="color:green;">chi trả</b>. Chi tiết bên dưới:'
            lines = [
                ('Mã bảng lương', rec.ma_bang_luong),
                ('Tháng/Năm', f'{rec.thang}/{rec.nam}'),
                ('Tổng thu nhập', f'{rec.tong_thu_nhap:,.0f} VNĐ'),
                ('Tổng khấu trừ', f'{rec.tong_khau_tru:,.0f} VNĐ'),
                ('Thuế TNCN', f'{rec.thue_tncn:,.0f} VNĐ'),
                ('Thực lĩnh', f'<b style="color:green;">{rec.thuc_linh:,.0f} VNĐ</b>'),
            ]
            body = service._build_email_html(title, greeting, lines)
            ok, msg = service.send_email(email, title, body, from_name='Hệ thống Nhân sự')
            rec.message_post(body=msg)

    def action_ve_nhap(self):
        self.write({'trang_thai': 'nhap'})

    def action_tinh_luong_tu_hop_dong(self):
        """Lấy lương từ hợp đồng lao động đang hiệu lực."""
        for rec in self:
            hop_dong = self.env['hop_dong_lao_dong'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('trang_thai', 'in', ['hieu_luc', 'sap_het_han']),
            ], order='ngay_bat_dau desc', limit=1)
            if hop_dong:
                rec.write({
                    'luong_co_ban': hop_dong.luong_co_ban,
                    'phu_cap_an': hop_dong.phu_cap_an,
                    'phu_cap_di_lai': hop_dong.phu_cap_di_lai,
                    'phu_cap_khac': hop_dong.phu_cap_dien_thoai + hop_dong.phu_cap_khac,
                })
