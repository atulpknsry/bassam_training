# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError

class BiMulticompanyCorrection(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        for rec in self.order_line:
            quant_id = self.env['stock.quant'].search([('product_id','=',rec.product_id.id),('location_id','=',self.env['stock.location'].search([('complete_name','=','Class/Stock')]).id)])
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
                    'partner_id': self.env['res.partner'].search([('email','=','info@helix.com')]).id,
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
                    'partner_id': self.env['res.partner'].search([('email','=','info@classic.com')]).id,
                    'company_id': self.env['res.company'].search([('email','=','info@helix.com')]).id,
                    'warehouse_id': self.env['stock.warehouse'].search([('code','=','Helix')]).id,
                    'order_line': so2_lines,
                }
                so2_id = self.env['sale.order'].create(so2_vals)
        
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'date_order': fields.Datetime.now()
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()
        return True
