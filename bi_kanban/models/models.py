# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class kanban(models.Model):
    _name = 'kanban'
    _description = 'kanban'

    name = fields.Char(string='Name')
    age = fields.Selection([
        ('old', 'Old'),
        ('mid', 'Middle'),
        ('new', 'New'),
        ('future','Future')
    ], string='Age', group_expand="_read_group_stage_ids")
    stage_id = fields.Many2one('pipeline.stages', string='Stage', group_expand="_read_group_stage_ids")
    value = fields.Integer(string='Value')
    market = fields.Selection([
        ('low', 'Low'),
        ('good', 'Good'),
        ('high', 'High'),
        ('dead', 'Dead')
    ], string='Market')
    image = fields.Binary(string='Image')
    rating = fields.Selection([
        ('0', 'No Rating'),
        ('1', 'Bad'),
        ('2', 'Average'),
        ('3', 'Good')
    ], string='Rating')

    def _read_group_stage_ids(self, states, domain, order):
        # var = self._fields['age'].selection
        # stage_ids = dict(var)
        stage_ids = self.env['pipeline.stages'].search([])
        return stage_ids


class PipelineStages(models.Model):
    _name = 'pipeline.stages'
    _description = 'description'
    _rec_name = 'pipeline_stage'
    
    pipeline_stage = fields.Char()

    