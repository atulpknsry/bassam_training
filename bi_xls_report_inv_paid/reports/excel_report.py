# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import xlsxwriter

class SaleOrderExcelReport(models.AbstractModel):
    _name = 'report.bi_xls_report_inv_paid.excel_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        ws = workbook.add_worksheet('Sale Report')
        
        format1_header = workbook.add_format({'bold':True, 'align':'center'})
        format2_align_right = workbook.add_format({'align':'right'})
        format3_currency = workbook.add_format({'num_format':'#,##0.00'})
        format4_title = workbook.add_format({'bold':True, 'align':'center', 'font_size':24})
        
        ws.set_column('A:A',12)
        ws.set_column('B:B',15)
        ws.set_column('C:C',15)
        ws.set_column('D:D',15)
        ws.set_column('E:E',20)
        ws.set_column('F:F',20)
        ws.set_column('G:G',25)
        ws.set_column('H:H',10)
        ws.set_column('I:I',10)
        ws.set_row(0, 32)

        row = 1

        ws.merge_range('A1:I1','Sale Order',format4_title)

        row = row + 1
        ws.write('A%s'%row,'Quotation',format1_header)
        ws.write('B%s'%row,'Create Date',format1_header)
        ws.write('C%s'%row,'Delivery Date',format1_header)
        ws.write('D%s'%row,'Expected Date',format1_header)
        ws.write('E%s'%row,'Customer',format1_header)
        ws.write('F%s'%row,'Salesperson',format1_header)
        ws.write('G%s'%row,'Company',format1_header)
        ws.write('H%s'%row,'Total',format1_header)
        ws.write('I%s'%row,'Status',format1_header)

        so_ids = self.env['sale.order'].search([('create_date','>=',data['form']['start_date']),('create_date','<=',data['form']['end_date']),('state','=','sale')])
        am_ids = self.env['account.move'].search([('invoice_payment_state','=','paid')])
        row = row + 1
        for rec in so_ids:
            invoices = rec.mapped('invoice_ids')
            for data in invoices:
                if data in am_ids:
                    flag = True
                else:
                    flag = False
            if flag == True:
                ws.write('A%s' % row,rec.name,format2_align_right)
                ws.write('B%s' % row,rec.create_date.strftime("%m/%d/%Y"),format2_align_right)
                ws.write('C%s' % row,rec.commitment_date,format2_align_right)
                ws.write('D%s' % row,rec.expected_date.strftime("%m/%d/%Y"),format2_align_right)
                ws.write('E%s' % row,rec.partner_id.name,format2_align_right)
                ws.write('F%s' % row,rec.user_id.name,format2_align_right)
                ws.write('G%s' % row,rec.company_id.name,format2_align_right)
                ws.write('H%s' % row,rec.amount_total,format3_currency)
                ws.write('I%s' % row,rec.state,format2_align_right)
                row = row + 1

