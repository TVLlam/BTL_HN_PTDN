# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gmail_notification_email = fields.Char(
        "Gmail gửi thông báo",
        config_parameter='gmail_notification_email',
        help="Địa chỉ Gmail dùng để gửi email thông báo tự động"
    )
    gmail_notification_password = fields.Char(
        "Gmail App Password",
        config_parameter='gmail_notification_password',
        help="App Password của Gmail (16 ký tự). Lấy tại: Google Account > Security > 2-Step Verification > App passwords"
    )
