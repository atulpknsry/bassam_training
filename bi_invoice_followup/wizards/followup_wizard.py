# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class FollowupWizard(models.TransientModel):
    _name = 'followup.wizard'
    _description = 'description'

    date = fields.Date(string='Date')
    remarks = fields.Text(string='Remarks')
    current_id = fields.Many2one(comodel_name='account.move')

    def submit_followup_remarks(self):
        acc_move_obj = self.env['account.move'].search([('id','=',self.current_id.id)])
        lines=[]
        # datas = {'date':self.date}
        # datas['remarks'] = self.remarks
        lines.append((0,0,{'date':self.date,'remarks':self.remarks}))
        acc_move_obj.write({
            'followup_ids':lines,
        })