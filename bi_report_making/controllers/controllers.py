# -*- coding: utf-8 -*-
# from odoo import http


# class ReportMaking(http.Controller):
#     @http.route('/report_making/report_making/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_making/report_making/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_making.listing', {
#             'root': '/report_making/report_making',
#             'objects': http.request.env['report_making.report_making'].search([]),
#         })

#     @http.route('/report_making/report_making/objects/<model("report_making.report_making"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_making.object', {
#             'object': obj
#         })
