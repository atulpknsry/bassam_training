# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import date

class BiQueryWizard(models.TransientModel):
    _name = 'bi.query.wizard'

    date_from = fields.Date(string='From', default=date.today(), required=True)
    date_to = fields.Date(string='To', default=date.today(), required=True)

    def get_report(self):
        self._cr.execute("SELECT * FROM sale_order")
        datas = self._cr.fetchall()
        self.env.ref('bi_query.action_report_bi_query').report_action(data=datas)