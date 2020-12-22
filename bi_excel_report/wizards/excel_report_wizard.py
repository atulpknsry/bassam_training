# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ExcelReportWizard(models.TransientModel):
    _name = 'excel.report.wizard'
    _description = 'Wizard for creating excel report'

    start_date = fields.Datetime(string='Start Date', help="Enter the first date", required=True)
    end_date = fields.Datetime(string='End Date', help="Enter the last date", required=True)

    def get_excel_report(self):

        if self.start_date > self.end_date :
            raise UserError("Start date should be before end date")
    
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'sale.order'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('bi_excel_report.action_report_excel').report_action(self, data=datas, config=False)
