# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

# Employee Training model


class BiEmployeeTraining(models.Model):
    _name = 'bi.employee.training'
    _description = 'Employee can request for a training'
    _rec_name = 'name'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search(
            [('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char(string='Subject', required=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', default=_default_employee,
                                  required=True)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True)
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('approve', 'Approve'), ('assign employee', 'Assign Employee'), ('refuse', 'Refused')
                              ], string='State', default='draft')
    training_ids = fields.One2many(
        comodel_name='bi.employee.training.line', inverse_name='training_id')
    refusal_reason = fields.Char(string='Refusal Reason',readonly=True)

    def action_request(self):
        self.state = 'requested'

    def action_approve(self):
        self.state = 'approve'

    def action_assign_employee(self):
        view = self.env.ref(
            'bi_employee_training.employee_training_wizard_view')
        return {
            'name': _('Employee Training'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bi.employee.training.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_employee_training_id': self.id,
                        },
        }

    def action_refused(self):
        view = self.env.ref(
            'bi_employee_training.employee_training_refusal_wizard_view')
        return {
            'name': _('Employee Training Refusal Reason'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bi.training.refuse.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {'default_training_id': self.id,
                        },
        }
    
    def return_assigned_trainees(self):
        training_ids = []
        result = self.env['bi.employee.training'].search([])
        for rec in result:
            partner_ids = rec.mapped('training_ids.partner_id.id')
            if self.env.user.partner_id.id in partner_ids:
                training_ids.append(rec.id)
        return {
            'name': 'Requests',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'domain': [('id', 'in',training_ids)],
            'res_model': 'bi.employee.training',
            'target': 'current'
        }

# Employee Training model
class BiEmployeeTrainingLine(models.Model):
    _name = 'bi.employee.training.line'
    _description = 'Employee can request for a training'

    partner_id = fields.Many2one('res.partner', string='Trainer',readonly=True)
    date = fields.Date(string='Date',readonly=True)
    time = fields.Char(string='Time',readonly=True)
    training_id = fields.Many2one('bi.employee.training', string='Training')


# Employee training wizard
class BiEmployeeTrainingWizard(models.TransientModel):
    _name = 'bi.employee.training.wizard'
    _description = "Training wizard"

    wizard_ids = fields.One2many(
        'bi.employee.training.wizard.line', 'training_wizard_id')
    employee_training_id = fields.Many2one(
        'bi.employee.training', string='Training')

    def action_confirm(self):
        val = []
        if self.wizard_ids:
            for line in self.wizard_ids:
                val.append((0, 0, {'partner_id': line.partner_id.id,
                                   'date': line.date,
                                   'time': line.time,
                                   }))
        values = self.env['bi.employee.training'].search(
            [('id', '=', self.employee_training_id.id)], limit=1)
        training_line = {
            'training_ids': val,
            'state' : 'assign employee',
        }
        values.write(training_line)


# Training wizard line
class BiEmployeeTrainingWizardLine(models.TransientModel):
    _name = 'bi.employee.training.wizard.line'
    _description = "Training wizard Line"

    partner_id = fields.Many2one('res.partner', string='Trainer')
    date = fields.Date(string='Date')
    time = fields.Char(string='Time')
    training_wizard_id = fields.Many2one('bi.employee.training.wizard')
