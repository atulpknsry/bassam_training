# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import date

class BiQueryWizard(models.TransientModel):
    _name = 'bi.query.wizard'

    date_from = fields.Date(string='From', default=date.today(), required=True)
    date_to = fields.Date(string='To', default=date.today(), required=True)

    def get_report(self):
        data={
            'ids':self.ids,
            'model':self._name,
            'form':{
                'date_from':self.date_from,
                'date_to':self.date_to,
            },
        }
        return self.env.ref('bi_query.action_report').report_action(self, data=data)
    
class QueryReport(models.AbstractModel):
    _name='report.bi_query.report_template'

    def _get_report_values(self, docids, data):
        date_from=data['form']['date_from']
        date_to=data['form']['date_to']

        self.env.cr.execute(""" SELECT so.name AS quotation, rp.name AS customer, rp2.name AS salesperson, rc.name AS company, so.amount_total AS total
                                FROM sale_order AS so
                                JOIN res_partner AS rp ON so.partner_id = rp.id
                                JOIN res_users AS ru ON so.user_id = ru.id
                                JOIN res_partner AS rp2 ON ru.partner_id = rp2.id
                                JOIN res_company as rc ON ru.company_id = rc.id
                                WHERE so.create_date BETWEEN %s AND %s""",(str(date_from),(str(date_to)))
                            )
        values=self.env.cr.dictfetchall()

        return{
            'values':values
        }