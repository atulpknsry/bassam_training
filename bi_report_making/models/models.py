# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class report_making_sample_data(models.Model):
    _name = 'report.making.sample.data'
    _description = 'sample data to make report'

    name = fields.Char(string='Name')
    roll_no = fields.Integer(string='Roll No')

    