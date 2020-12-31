# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import smtplib
from datetime import datetime, date, timedelta
import base64

class BiEmail(models.Model):
    _name = 'bi.email'
       
    name = fields.Char()
    sender = fields.Many2one('res.users','Sender', default=lambda self: self.env.user, readonly=True)
    receiver = fields.Many2one('res.partner','Customer')
    # file = fields.Binary(string='File')

    def send_email(self):
        mail_template = self.env.ref('bi_email.email_template')

        date_to=date.today()
        date_from=date_to-timedelta(15)
        dataa={
            'form':{
                'date_from':date_from,
                'date_to':date_to,
            },
        }
        # so_ids = self.env['sale.order'].search([('create_date','>=',date_from),('create_date','<=',date_to)])
        # pdf = self.env.ref('bi_sale_order_report.action_report_sale_order').render_qweb_pdf(so_ids.ids)
        # obj = self.env['bi.query.wizard']
        pdf = self.env.ref('bi_query.action_report').render_qweb_pdf(self, data=dataa)
        b64_pdf = base64.b64encode(pdf[0])

        attachment = {
            'name':'Attachment',
            'datas':b64_pdf,
            'res_model':'bi.email',
            'type':'binary',
        }
        attach_id = self.env['ir.attachment'].create(attachment)
        mail_template.attachment_ids = [(6,0,[attach_id.id])]
        mail_template.send_mail(self.id,force_send=True)

class NoTemplateMail(models.Model):
    _name = 'no.template.mail'

    mail_to = fields.Many2one('res.partner','To')
    subject = fields.Char('Subject')
    body = fields.Text(string='Body')

    def send_wo_template(self):
        user_id = self._uid
        user_obj= self.env['res.users'].browse(user_id)
        email_to = self.mail_to.email
        vals={
            'email_to':email_to,
            'email_from':user_obj.email,
            'subject':self.subject,
            'body_html':self.body,
        }
        mail_id=self.env['mail.mail'].sudo().create(vals)
        mail_id.sudo().send()
