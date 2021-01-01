# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import datetime

class MultiCompanyDemo(models.Model):
    _name = 'multicompany.demo'

    partner_id = fields.Many2one('res.partner', string='Customer', required="1")
    date_order = fields.Datetime(string='Quotation Date',required="1", default=lambda self: datetime.now())
    order_line = fields.One2many('order.line', 'order_id', string='')
    so_id = fields.Many2one('sale.order',string='')

    def make_sale_order(self):
        so_obj = self.env['sale.order']
        lines = []
        for rec in self.order_line:
            line = {
                'product_id' : rec.product_id.id,
                'name' : rec.name,
                'product_uom_qty' : rec.product_uom_qty,
                'price_unit' : rec.price_unit,
            }
            lines.append((0,0,line))
        vals = {
            'partner_id' : self.partner_id.id,
            'date_order' : self.date_order,
            'order_line' : lines,
        }
        self.so_id = so_obj.create(vals)
        self.so_id.action_confirm()

class OrderLine(models.Model):
    _name = 'order.line'

    product_id = fields.Many2one('product.product', string='Product', required="1")
    name = fields.Text(string='Description', required="1")
    product_uom_qty = fields.Float(string='Quantity', required="1")
    price_unit = fields.Float(string='Unit Price', required="1")
    order_id = fields.Many2one('multicompany.demo', string='')