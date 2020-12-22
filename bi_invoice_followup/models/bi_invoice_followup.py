# -*- coding: utf-8 -*-
from datetime import date
from odoo import _, api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    followup_ids = fields.One2many('invoice.followup.lines', 'account_move_id', string='Invoice Followups')
    followup_state = fields.Boolean(string='', compute='_compute_followup_state')

    def _compute_followup_state(self):
        for rec in self:
            if ((rec.type == 'out_invoice')and(rec.invoice_payment_state == 'not_paid')and(rec.invoice_date_due < date.today())):
                rec.followup_state = True
            else:
                rec.followup_state = False

    def action_invoice_followup(self):
        return{
            'type':'ir.actions.act_window',
            'name':'Follow Up',
            'res_model':'followup.wizard',
            'view_mode':'form',
            'target':'new',
            'context': {'default_current_id': self.id},
        }
        


class InvoiceFollowupLines(models.Model):
    _name = 'invoice.followup.lines'
    _description = 'Invoice followup details'

    account_move_id = fields.Many2one('account.move')
    date = fields.Date(string="Date")
    remarks = fields.Char(string="Remarks")

    
    