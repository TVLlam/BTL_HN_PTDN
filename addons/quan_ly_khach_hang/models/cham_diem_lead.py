# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


class ChamDiemLead(models.Model):
    _name = 'cham_diem_lead'
    _description = 'Chấm điểm Lead tự động'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'tong_diem desc'
    _rec_name = 'khach_hang_id'

    khach_hang_id = fields.Many2one('khach_hang', string="Khách hàng", required=True, ondelete='cascade', tracking=True)
    nhan_vien_phu_trach_id = fields.Many2one(related='khach_hang_id.nhan_vien_phu_trach_id', string="NV phụ trách", store=True)

    # Điểm thành phần
    diem_tuong_tac = fields.Float(string="Điểm tương tác", compute='_compute_diem', store=True,
                                    help="Dựa trên số lần tương tác gần đây")
    diem_doanh_thu = fields.Float(string="Điểm doanh thu", compute='_compute_diem', store=True,
                                    help="Dựa trên doanh thu trong 12 tháng")
    diem_phan_hoi = fields.Float(string="Điểm phản hồi", compute='_compute_diem', store=True,
                                    help="Dựa trên phản hồi khảo sát")
    diem_trung_thanh = fields.Float(string="Điểm trung thành", compute='_compute_diem', store=True,
                                      help="Dựa trên thời gian gắn bó")
    diem_co_hoi = fields.Float(string="Điểm cơ hội", compute='_compute_diem', store=True,
                                 help="Dựa trên cơ hội đang mở")

    tong_diem = fields.Float(string="Tổng điểm", compute='_compute_diem', store=True, tracking=True)
    xep_hang = fields.Selection([
        ('nong', 'Nóng (Hot)'),
        ('am', 'Ấm (Warm)'),
        ('lanh', 'Lạnh (Cold)'),
        ('dong_bang', 'Đóng băng (Frozen)'),
    ], string="Xếp hạng", compute='_compute_diem', store=True, tracking=True)

    ngay_tinh_diem = fields.Datetime(string="Lần tính điểm cuối", readonly=True)
    ghi_chu = fields.Text(string="Ghi chú")

    _sql_constraints = [
        ('khach_hang_unique', 'unique(khach_hang_id)', 'Mỗi khách hàng chỉ có một bảng chấm điểm!')
    ]

    @api.depends('khach_hang_id')
    def _compute_diem(self):
        for rec in self:
            if not rec.khach_hang_id:
                rec.diem_tuong_tac = rec.diem_doanh_thu = rec.diem_phan_hoi = 0
                rec.diem_trung_thanh = rec.diem_co_hoi = rec.tong_diem = 0
                rec.xep_hang = 'dong_bang'
                continue

            kh = rec.khach_hang_id

            # 1. Điểm tương tác (max 25)
            tuong_tac_count = self.env['lich_su_tuong_tac'].search_count([
                ('khach_hang_id', '=', kh.id),
                ('ngay_tuong_tac', '>=', fields.Datetime.to_string(date.today() - timedelta(days=90)))
            ])
            rec.diem_tuong_tac = min(tuong_tac_count * 5, 25)

            # 2. Điểm doanh thu (max 30)
            doanh_thu = kh.doanh_thu_12_thang or 0
            if doanh_thu >= 1000000000:  # >= 1 tỷ
                rec.diem_doanh_thu = 30
            elif doanh_thu >= 500000000:
                rec.diem_doanh_thu = 25
            elif doanh_thu >= 200000000:
                rec.diem_doanh_thu = 20
            elif doanh_thu >= 50000000:
                rec.diem_doanh_thu = 15
            elif doanh_thu > 0:
                rec.diem_doanh_thu = 10
            else:
                rec.diem_doanh_thu = 0

            # 3. Điểm phản hồi khảo sát (max 15)
            khao_sat = self.env['khao_sat_hai_long'].search([
                ('khach_hang_id', '=', kh.id),
                ('trang_thai', '=', 'da_phan_hoi')
            ], order='ngay_phan_hoi desc', limit=1)
            if khao_sat and khao_sat.diem_trung_binh:
                rec.diem_phan_hoi = khao_sat.diem_trung_binh * 3  # max 5*3=15
            else:
                rec.diem_phan_hoi = 0

            # 4. Điểm trung thành (max 15) 
            hop_dong_count = self.env['hop_dong'].search_count([
                ('khach_hang_id', '=', kh.id),
                ('trang_thai', '=', 'hieu_luc')
            ])
            rec.diem_trung_thanh = min(hop_dong_count * 5, 15)

            # 5. Điểm cơ hội đang mở (max 15)
            co_hoi_count = self.env['co_hoi_ban_hang'].search_count([
                ('khach_hang_id', '=', kh.id),
                ('trang_thai', '=', 'mo')
            ])
            rec.diem_co_hoi = min(co_hoi_count * 5, 15)

            # Tổng điểm
            rec.tong_diem = rec.diem_tuong_tac + rec.diem_doanh_thu + rec.diem_phan_hoi + rec.diem_trung_thanh + rec.diem_co_hoi

            # Xếp hạng
            if rec.tong_diem >= 70:
                rec.xep_hang = 'nong'
            elif rec.tong_diem >= 40:
                rec.xep_hang = 'am'
            elif rec.tong_diem >= 15:
                rec.xep_hang = 'lanh'
            else:
                rec.xep_hang = 'dong_bang'

    def action_tinh_lai_diem(self):
        """Tính lại điểm thủ công"""
        self._compute_diem()
        self.write({'ngay_tinh_diem': fields.Datetime.now()})

    @api.model
    def _cron_tinh_diem_lead(self):
        """Cron job: Tính lại điểm cho toàn bộ khách hàng"""
        # Tạo bản ghi cho khách hàng chưa có
        existing_kh_ids = self.search([]).mapped('khach_hang_id.id')
        all_kh = self.env['khach_hang'].search([('id', 'not in', existing_kh_ids)])
        for kh in all_kh:
            self.create({'khach_hang_id': kh.id})
        
        # Tính lại tất cả
        all_records = self.search([])
        all_records._compute_diem()
        all_records.write({'ngay_tinh_diem': fields.Datetime.now()})
