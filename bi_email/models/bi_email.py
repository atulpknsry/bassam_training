# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import smtplib
class BiEmail(models.Model):
    _name = 'bi.email'
       
    name = fields.Char()
    sender = fields.Many2one('res.users','Sender', default=lambda self: self.env.user, readonly=True)
    receiver = fields.Many2one('res.partner','Customer')
    file = fields.Binary(string='File')

    def send_email(self):
        mail_template = self.env.ref('bi_email.email_template')
        attachment = {
            'name':'Attachment',
            'datas':self.file,
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
