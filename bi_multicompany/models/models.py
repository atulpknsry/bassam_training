# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import datetime, timedelta

class MultiCompanyDemo(models.Model):
    _name = 'multicompany.demo'

    partner_id = fields.Many2one('res.partner', string='Customer', required="1")
    date_order = fields.Datetime(string='Quotation Date',required="1", default=lambda self: datetime.now())
    order_line = fields.One2many('order.line', 'order_id', string='')
    so_id = fields.Many2one('sale.order',string='')

    def make_sale_order(self):
        lines = []
        for rec in self.order_line:
            line = {
                'product_id' : rec.product_id.id,
                'name' : rec.name,
                'product_uom_qty' : rec.product_uom_qty,
                'price_unit' : rec.price_unit,
            }
            quant_id = self.env['stock.quant'].search([('product_id','=',rec.product_id.id),('location_id','=',self.env['stock.location'].search([('complete_name','=','WH/Stock')]).id)])
            available_qty = self.env['stock.quant'].browse(quant_id.id).quantity
            if available_qty < rec.product_uom_qty :
                po_lines = []
                po_line = {
                    'product_id' : rec.product_id.id,
                    'name' : rec.name,
                    'product_qty' : rec.product_uom_qty,
                    'product_uom' : rec.product_id.uom_id.id,
                    'price_unit' : rec.price_unit,
                }
                po_lines.append((0,0,po_line))
                po_vals = {
                    'partner_id': self.env['res.partner'].search([('email','=','ceo@anothercompany')]).company_id,
                    # 'company_id': self.env['res.company'].search([('email','=','info@mycompany.com')]).id,
                    'date_planned' : self.date_order + timedelta(10),
                    'order_line': po_lines,
                }
                po_id = self.env['purchase.order'].create(po_vals)
                po_id.button_confirm()
                so2_lines = []
                so2_line = {
                    'product_id' : rec.product_id.id,
                    'name' : rec.name,
                    'product_uom_qty' : rec.product_uom_qty,
                    'price_unit' : rec.price_unit,
                }
                so2_lines.append((0,0,so2_line))
                so2_vals = {
                    'partner_id': self.env['res.partner'].search([('email','=','ceo@mycompany')]).id,
                    'company_id': self.env['res.company'].search([('email','=','info@anothercompany.com')]).id,
                    'warehouse_id': self.env['stock.warehouse'].search([('code','=','Anoth')]).id,
                    'order_line': so2_lines,
                }
                so2_id = self.env['sale.order'].create(so2_vals)
                so2_id.action_confirm()

            lines.append((0,0,line))
        vals = {
            'partner_id' : self.partner_id.id,
            'date_order' : self.date_order,
            # 'company_id' : self.env['res.company'].search([('name','=','My Company')]).id,
            # 'warehouse_id': self.env['stock.warehouse'].search([('code','=','WH')]).id,
            'order_line' : lines,
        }
        self.so_id = self.env['sale.order'].create(vals)
        self.so_id.action_confirm()

class OrderLine(models.Model):
    _name = 'order.line'

    product_id = fields.Many2one('product.product', string='Product', required="1")
    name = fields.Text(string='Description', required="1")
    product_uom_qty = fields.Float(string='Quantity', required="1")
    price_unit = fields.Float(string='Unit Price', required="1")
    order_id = fields.Many2one('multicompany.demo', string='')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name