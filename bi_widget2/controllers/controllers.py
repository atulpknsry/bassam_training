# -*- coding: utf-8 -*-
# from odoo import http


# class BiWidget2(http.Controller):
#     @http.route('/bi_widget2/bi_widget2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bi_widget2/bi_widget2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bi_widget2.listing', {
#             'root': '/bi_widget2/bi_widget2',
#             'objects': http.request.env['bi_widget2.bi_widget2'].search([]),
#         })

#     @http.route('/bi_widget2/bi_widget2/objects/<model("bi_widget2.bi_widget2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bi_widget2.object', {
#             'object': obj
#         })
