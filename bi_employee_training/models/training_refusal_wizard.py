# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class BiTrainingRefusalWizard(models.TransientModel):
    _name = 'bi.training.refuse.wizard'
    _description = "Refusal wizard"

    refusal_reason = fields.Char(string='Refusal Reason')
    training_id = fields.Many2one('bi.employee.training', string='Employee Training')

    def action_confirm(self):
        training = self.env['bi.employee.training'].search([('id','=',self.training_id.id)],limit=1)
        training.write({'refusal_reason': self.refusal_reason,
                      'state': 'refuse',
                      })

