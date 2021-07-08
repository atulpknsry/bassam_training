# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class BiPartnerStatement(models.TransientModel):
    _name = 'bi.partner.statement'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    partner_id = fields.Many2one('res.partner', string='Customer')
    account_type = fields.Selection([('payable','Payable'),('receivable','Receivable')],'Account Type',)

    def get_statement(self):
        data={
            'ids':self.ids,
            'model':self._name,
            'form':{
                'date_from':self.date_from,
                'date_to':self.date_to,
                'partner_id':self.partner_id.id,
                'partner_name':self.partner_id.name,
                'account_type':self.account_type,
            },
        }
        return self.env.ref('bi_partner_statement.action_report_bi_partner_statement').report_action(self, data=data)

class PartnerSatementReport(models.AbstractModel):
    _name='report.bi_partner_statement.report_template_partner_statement'

    def _get_report_values(self, docids, data):
        self.env.cr.execute("""
            SELECT sum(ml.credit-ml.debit) as balance
            FROM account_move_line as ml
            JOIN res_partner as rp on ml.partner_id=rp.id
            WHERE ml.partner_id=%s AND ml.date <= %s
            """,(data['form']['partner_id'],data['form']['date_from']))

        initial_balance=self.env.cr.dictfetchall()[0]['balance']
        if not initial_balance:
            initial_balance=0.0            
        temp_bal=initial_balance

        self.env.cr.execute("""
            SELECT p.name as partner_name, m.ref as ref, l.name as name, l.date as date, j.name as journal, l.debit as debit, l.credit as credit, l.debit-l.credit as balance_delta
            FROM account_move_line AS l
            JOIN account_move AS m ON l.move_id=m.id
            JOIN res_partner AS p ON l.partner_id=p.id
            JOIN account_journal AS j ON l.journal_id=j.id
            JOIN account_account AS a ON l.account_id=a.id
            WHERE l.partner_id=%s AND a.reconcile=True AND l.date BETWEEN %s AND %s
            ORDER BY l.date
            """,(data['form']['partner_id'],data['form']['date_from'],data['form']['date_to']))

        values = self.env.cr.dictfetchall()

        for vals in values:
            temp_bal=temp_bal+vals['balance_delta']
            vals['balance']=temp_bal

        final_balance=temp_bal

        return{
            'partner_name':data['form']['partner_id'],
            'date_from':data['form']['date_from'],
            'date_to':data['form']['date_to'],
            'initial_balance':initial_balance,
            'final_balance':final_balance,
            'values':values,
        }