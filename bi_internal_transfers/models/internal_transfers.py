# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
class InternalTransfers(models.Model):
    _name = 'internal.transfers'

    name = fields.Char(string='Reference')
    origin = fields.Char(string='Source Document')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed','Waiting'),
        ('assigned','Ready'),
        ('done','Done'),
    ], string='Status', default="draft")
    scheduled_date = fields.Datetime(string='Scheduled Date')
    location_id = fields.Many2one('stock.location', string='Source Location')
    location_dest_id = fields.Many2one('stock.location', string='Destination Location')
    move_lines = fields.One2many('stock.move', 'picking_id', string='Stock Moves')
    picking_type_id = fields.Many2one('stock.picking.type', string='Operation Type')
    picking_id = fields.Many2one('stock.picking')
    move_id = fields.Many2one('stock.move')
    move_line_ids = fields.One2many('stock.move.line', 'picking_id', string='Operations')
    product_line_ids = fields.One2many('product.lines','internal_transfers_id')

    def confirm(self):
        self.state = 'confirmed'

    def reserve(self):
        self.state = 'assigned'
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        location_transit = self.env['stock.location'].browse(40)
        for rec in self:
            lines=[]
            for line in self.product_line_ids:
                vals={'product_id':line.product_id.id}
                vals['product_uom_qty'] = line.product_uom_qty
                lines.append(vals)
            picking_vals={
                'origin':rec.origin,
                'move_type':'direct',
                'state':rec.state,
                'scheduled_date':rec.scheduled_date,
                'date':rec.scheduled_date,
                'location_id':rec.location_id.id,
                'location_dest_id':location_transit.id,
                'picking_type_id':rec.picking_type_id.id,
                'create_date':datetime.now().strftime('%d-%m-%Y'),
                'write_date':rec.scheduled_date,
                'move_line_ids_without_package':lines,
            }
            rec.picking_id = picking_obj.create(picking_vals)
            rec.write({'name':rec.picking_id.name})
            for line in rec.product_line_ids:
                move_vals = {
                    'name':rec.name,
                    'create_date':datetime.now().strftime('%d-%m-%Y'),
                    'date':rec.scheduled_date,
                    'date_expected':rec.scheduled_date,
                    'product_id':line.product_id.id,
                    'product_uom_qty':line.product_uom_qty,
                    'location_id':rec.location_id.id,
                    'location_dest_id':location_transit.id,
                    'picking_id':rec.picking_id.id,
                    'state':rec.state,
                    'origin':rec.origin,
                    'picking_type_id':rec.picking_type_id.id,
                    'product_uom':1,
                }
                rec.move_id = move_obj.create(move_vals)
            rec.picking_id.action_assign()

    def validate(self):
        pass

class ProductLines(models.Model):
    _name = 'product.lines'
    
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Demand')
    reserved_availability = fields.Float(string='Reserved')
    quantity_done = fields.Float(string='Done')

    internal_transfers_id = fields.Many2one('internal.transfers')