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
    scheduled_date = fields.Datetime(string='Scheduled Date', required=True)
    location_id = fields.Many2one('stock.location', string='Source Location')
    location_dest_id = fields.Many2one('stock.location', string='Destination Location')
    move_lines = fields.One2many('stock.move', 'picking_id', string='Stock Moves')
    picking_type_id = fields.Many2one('stock.picking.type', string='Operation Type')
    move_line_id = fields.Many2one(comodel_name='stock.move.line')
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
        location_transit = self.env['stock.location'].search([('name','=','CustomTransit')])
        for rec in self:
            picking_vals={
                'origin':rec.origin,
                'scheduled_date':rec.scheduled_date,
                'date':rec.scheduled_date,
                'location_id':rec.location_id.id,
                'location_dest_id':location_transit.id,
                'picking_type_id':rec.picking_type_id.id,
            }
            rec.picking_id = picking_obj.sudo().create(picking_vals)
            rec.write({'name':rec.picking_id.name})
            for line in rec.product_line_ids:
                move_vals = {
                    'name':rec.name,
                    'date':rec.scheduled_date,
                    'date_expected':rec.scheduled_date,
                    'product_id':line.product_id.id,
                    'product_uom_qty':line.product_uom_qty,
                    'location_id':rec.location_id.id,
                    'location_dest_id':location_transit.id,
                    'picking_id':rec.picking_id.id,
                    'origin':rec.origin,
                    'picking_type_id':rec.picking_type_id.id,
                    'product_uom':(self.env['uom.uom'].search([('name','=','Units')]).id),
                }
                rec.move_id = move_obj.sudo().create(move_vals)
                move_line_vals = {
                    'picking_id':rec.picking_id.id,
                    'move_id':rec.move_id.id,
                    'product_id':line.product_id.id,
                    'product_uom_id':1,
                    'product_uom_qty':line.product_uom_qty,
                    'qty_done':line.product_uom_qty,
                    'date':rec.scheduled_date,
                    'location_id':rec.location_id.id,
                    'location_dest_id':location_transit.id,
                    'reference':rec.name,
                }
                move_line_obj = self.env['stock.move.line']
                self.move_line_id = move_line_obj.create(move_line_vals)
            rec.picking_id.sudo().action_assign()
            self.env['stock.immediate.transfer'].sudo().create({'pick_ids': [(4, rec.picking_id.id)]}).process()
            quant = self.env['stock.quant'].search([])
            for rec in quant:
                qty = rec.quantity
                rec.sudo().write({'reserved_quantity':qty})

        self.state = 'assigned'
            
    
    def validate(self):        
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        location_transit = self.env['stock.location'].search([('name','=','CustomTransit')])
        for rec in self:
            lines=[]
            for line in self.product_line_ids:
                vals={
                    'product_id':line.product_id.id,
                    'product_uom_qty':line.product_uom_qty,
                    }
                lines.append(vals)
            picking_vals={
                'origin':rec.origin,
                'move_type':'direct',
                'state':rec.state,
                'scheduled_date':rec.scheduled_date,
                'date':rec.scheduled_date,
                'location_id':location_transit.id,
                'location_dest_id':rec.location_dest_id.id,
                'picking_type_id':rec.picking_type_id.id,
                'create_date':datetime.now().strftime('%d-%m-%Y'),
                'write_date':rec.scheduled_date,
                # 'move_line_ids_without_package':[(0,0,lines)],
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
                    'location_id':location_transit.id,
                    'location_dest_id':rec.location_dest_id.id,
                    'picking_id':rec.picking_id.id,
                    'state':rec.state,
                    'origin':rec.origin,
                    'picking_type_id':rec.picking_type_id.id,
                    'product_uom':1,
                }
                rec.move_id = move_obj.create(move_vals)
                move_line_vals = {
                    'picking_id':rec.picking_id.id,
                    'move_id':rec.move_id.id,
                    'product_id':line.product_id.id,
                    'product_uom_id':1,
                    'product_uom_qty':line.product_uom_qty,
                    'qty_done':line.product_uom_qty,
                    'date':rec.scheduled_date,
                    'location_id':location_transit.id,
                    'location_dest_id':rec.location_dest_id.id,
                    'reference':rec.name,
                }
                move_line_obj = self.env['stock.move.line']
                self.move_line_id = move_line_obj.create(move_line_vals)
            rec.picking_id.action_assign()
            self.env['stock.immediate.transfer'].create({'pick_ids': [(4, rec.picking_id.id)]}).process()
            quant = self.env['stock.quant'].search([])
            for rec in quant:
                qty = rec.quantity
                rec.sudo().write({'reserved_quantity':qty})    
        self.state = 'done'

    def return_request(self):
        return {
            'name': 'Requests',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'confirmed')],
            'res_model': 'internal.transfers',
            'target': 'current'
        }

    def return_approve(self):
        return {
            'name': 'Approve',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'confirmed')],
            'res_model': 'internal.transfers',
            'target': 'current'
        }

    def return_delivery(self):
        return {
            'name': 'Delivery',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('state', '=', 'assigned')],
            'res_model': 'internal.transfers',
            'target': 'current'
        }


class ProductLines(models.Model):
    _name = 'product.lines'
    
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_qty = fields.Float(string='Demand')
    reserved_availability = fields.Float(string='Reserved')
    quantity_done = fields.Float(string='Done')

    internal_transfers_id = fields.Many2one('internal.transfers')