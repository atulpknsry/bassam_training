# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import smtplib
from datetime import date, timedelta
import base64

class BiEmailXlsx(models.Model):
    _name = 'bi.email.xlsx'

    sender = fields.Many2one('res.users', string='From', default=lambda self: self.env.user, readonly="1")
    receiver = fields.Many2one('res.partner', string='To')

    def send_email(self):
        date_to = date.today()
        date_from = date_to-timedelta(15)
        dataa = {
            'form' : {
                'start_date' : date_from,
                'end_date' : date_to
            }
        }
        report = self.env.ref('bi_excel_report.action_report_excel').render_xlsx(self, data=dataa)
        attach = base64.b64encode(report[0])
        attachment = {
            'name' : 'Excel Report',
            'datas' : attach,
            'res_model' : 'bi.email.xlsx',
            'type' : 'binary'
        }
        attach_id = self.env['ir.attachment'].create(attachment)
        mail_template = self.env.ref('bi_email_xlsx.xlsx_email_template')
        mail_template.attachment_ids = [(6,0,[attach_id.id])]
        mail_template.send_mail(self.id, force_send=True)