# -*- coding: utf-8 -*-
import logging
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

# Đường dẫn .env
_ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '.env')


def _load_env():
    """Đọc biến môi trường từ file .env"""
    result = {}
    env_path = os.path.normpath(_ENV_PATH)
    if os.path.isfile(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    result[key.strip()] = val.strip()
    return result


class EmailNotificationService(models.AbstractModel):
    _name = 'email.notification.service'
    _description = 'Dịch vụ gửi email thông báo qua Gmail'

    def _get_gmail_config(self):
        """Lấy cấu hình Gmail từ .env hoặc ir.config_parameter"""
        env_vars = _load_env()
        email = (
            os.environ.get('GMAIL_EMAIL')
            or env_vars.get('GMAIL_EMAIL')
            or self.env['ir.config_parameter'].sudo().get_param('gmail_notification_email', '')
        )
        password = (
            os.environ.get('GMAIL_APP_PASSWORD')
            or env_vars.get('GMAIL_APP_PASSWORD')
            or self.env['ir.config_parameter'].sudo().get_param('gmail_notification_password', '')
        )
        return email, password

    def send_email(self, to_email, subject, body_html, from_name=None):
        """
        Gửi email thông báo qua Gmail SMTP.
        Returns: (bool success, str message)
        """
        sender_email, sender_password = self._get_gmail_config()
        if not sender_email or not sender_password:
            _logger.warning("Email notification: Chưa cấu hình GMAIL_EMAIL / GMAIL_APP_PASSWORD")
            return False, "Chưa cấu hình Gmail. Vui lòng thiết lập trong Cài đặt > Email thông báo."

        if not to_email:
            return False, "Không có email người nhận."

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{from_name} <{sender_email}>" if from_name else sender_email
            msg["To"] = to_email
            msg.attach(MIMEText(body_html, "html", "utf-8"))

            env_vars = _load_env()
            smtp_host = os.environ.get('SMTP_HOST') or env_vars.get('SMTP_HOST') or 'smtp.gmail.com'
            smtp_port = int(os.environ.get('SMTP_PORT') or env_vars.get('SMTP_PORT') or 587)
            use_tls = smtp_host != 'localhost'

            with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                if use_tls:
                    server.starttls()
                if sender_password:
                    server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, msg.as_string())

            _logger.info("Email sent to %s: %s", to_email, subject)
            return True, f"Đã gửi email đến {to_email}"
        except smtplib.SMTPAuthenticationError:
            err = "Lỗi xác thực Gmail. Kiểm tra GMAIL_EMAIL và GMAIL_APP_PASSWORD trong .env"
            _logger.error(err)
            return False, err
        except Exception as e:
            err = f"Lỗi gửi email: {str(e)}"
            _logger.error(err)
            return False, err

    def _build_email_html(self, title, greeting, content_lines, footer_name="Hệ thống ERP"):
        """Tạo HTML email đẹp, chuẩn hóa."""
        rows = ""
        for label, value in content_lines:
            rows += f'<tr><td style="padding:6px 12px;font-weight:bold;color:#555;">{label}</td><td style="padding:6px 12px;">{value}</td></tr>'

        return f"""
        <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;">
            <div style="background:#875A7B;color:#fff;padding:18px 24px;">
                <h2 style="margin:0;font-size:20px;">{title}</h2>
            </div>
            <div style="padding:24px;">
                <p>{greeting}</p>
                <table style="width:100%;border-collapse:collapse;margin:16px 0;background:#f9f9f9;border-radius:6px;">
                    {rows}
                </table>
            </div>
            <div style="background:#f5f5f5;padding:12px 24px;font-size:12px;color:#888;text-align:center;">
                {footer_name} &bull; Email tự động, vui lòng không trả lời.
            </div>
        </div>
        """
