# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


# inherited po
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    crm_id = fields.Many2one(comodel_name='crm.lead', string='')


# inherited crm
class CRMLead(models.Model):
    _inherit = 'crm.lead'
    
    # number of rfq by same lead
    rfq_count = fields.Integer(string='RFQ', compute='get_rfq_count')
    
    # get count of po by same lead
    def get_rfq_count(self):
        po_obj = self.env['purchase.order']
        for rec in self:
            po_list = po_obj.search([('crm_id','=',self.id)])
            rec.rfq_count = len(po_list)
    
    # make a po
    def action_new_rfq(self):
        return{
            'res_model':'vendor.wizard',
            'view_mode':'form',
            'type':'ir.actions.act_window',
            'target':'new',
            'context':{'default_current_id':self.id},
        }   

    # view po by same lead
    def action_view_po(self):
        po_obj = self.env['purchase.order']
        po_id = po_obj.search([('crm_id','=',self.id)])
        for rec in self:
            if(rec.rfq_count == 1):
                return{
                    'res_model':'purchase.order',
                    'res_id':po_id.id,
                    # 'domain':[('crm_id','=',self.id)],
                    'view_mode':'form',
                    'type':'ir.actions.act_window',
                }
            else:
                return{
                    'res_model':'purchase.order',
                    'domain':[('crm_id','=',self.id)],
                    'view_mode':'tree,form',
                    'type':'ir.actions.act_window',
                }


# wizard to accept vendor & product details
class VendorWizard(models.TransientModel):
    _name = 'vendor.wizard'
    _description = 'vendor wizard'

    partner_id = fields.Many2one('res.partner', string='Vendor')
    partner_ref = fields.Char(string='Vendor Reference')
    date_order = fields.Datetime(string='Order Date',default=lambda self: fields.datetime.now())
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)
    product_detail_line = fields.One2many(comodel_name='product.detail',inverse_name='product_detail_id',string='')
    rfq_id = fields.Many2one('purchase.order', string='')
    current_id = fields.Many2one('crm.lead',string='')

    def action_submit(self):
        po=self.env['purchase.order']
        lines=[]
        vals={}
        for line in self.product_detail_line:
            lines.append((0,0,{
                'product_id':line.product_id.id,
                'name':line.name,
                'product_qty':line.product_qty,
                'product_uom':1,
                'price_unit':line.price_unit,
            }))
        for rec in self:
            vals={
                'partner_id':self.partner_id.id,
                'partner_ref':self.partner_ref,
                'date_order':self.date_order,
                'company_id':self.company_id.id,
                'date_planned':fields.datetime.now(),
                'crm_id':self.current_id.id,
                'order_line':lines,                
            }
            rec.rfq_id = po.create(vals)
        

        # show submitted po for further action
        return{
            'name':('purchase_order_action_generic'),
            'res_model':'purchase.order',
            'res_id':self.rfq_id.id,
            'view_mode':'form',
            'type':'ir.actions.act_window',
        }

# product line to enter product details
class ProductDetail(models.TransientModel):
    _name = 'product.detail'
    _description = 'product details line'
    
    product_detail_id = fields.Many2one('vendor.wizard', string='')
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char(string='Description')
    product_qty = fields.Float(string='Quantity', digits=(4, 3))
    price_unit = fields.Float(string='Unit Price', digits=(3, 2))