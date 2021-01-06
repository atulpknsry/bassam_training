# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools

class BiViewSQL(models.Model):
    _name = 'bi.view.sql'
    _auto = False

    quotation = fields.Char(string='Quatation Number', readonly=True)
    date = fields.Datetime(string='Date', readonly=True)
    customer = fields.Char(string='Customer', readonly=True)
    salesperson = fields.Char(string='Salesperson', readonly=True)
    company = fields.Char(string='Company', readonly=True)
    total = fields.Float(string='Total', readonly=True)
    residual = fields.Float(string='Invoiced Due')
    picking = fields.Char(string='Picking')

    def init(self):
        tools.drop_view_if_exists(self.env.cr,'bi_view_sql')
        self.env.cr.execute("""CREATE OR REPLACE VIEW bi_view_sql AS (
            SELECT
            row_number() OVER() as id,
            so.name as quotation,
            so.create_date as date,
            rp.display_name as customer,
            rp2.name as salesperson,
            rc.name as company,
            so.amount_total as total,
            ac.amount_residual as residual,
            sp.name as picking
            FROM sale_order as so
            JOIN res_partner as rp ON so.partner_id = rp.id
            JOIN res_users as ru ON so.user_id = ru.id
            JOIN res_partner as rp2 ON ru.partner_id = rp2.id
            JOIN res_company as rc ON so.company_id = rc.id
            JOIN account_move as ac ON so.name = ac.invoice_origin
            JOIN stock_picking as sp ON so.name = sp.origin
            WHERE so.state = 'sale')
            """)
