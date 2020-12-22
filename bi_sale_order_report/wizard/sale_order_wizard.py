# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class SaleOrderWizard(models.TransientModel):
    _name = 'sale.order.wizard'

    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    cust_id = fields.Many2one(comodel_name='res.partner', string='Customer')
     
    def action_get_report(self):

        if self.start_date > self.end_date:
            raise UserError("Start date must be lower than End date")

        domain=[('create_date','>=',self.start_date),('create_date','<=',self.end_date)]
        
        if(self.cust_id):
            domain.append(('partner_id','=',self.cust_id.id))
        
        so_ids=self.env['sale.order'].search(domain)
        
        if not so_ids:
            raise UserError("No records found")

        return self.env.ref('bi_sale_order_report.action_report_sale_order').report_action(so_ids)
