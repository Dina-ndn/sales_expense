# -*- coding: utf-8 -*-
# from odoo import http


# class WaaneizaSaleExpense(http.Controller):
#     @http.route('/waaneiza_sale_expense/waaneiza_sale_expense', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/waaneiza_sale_expense/waaneiza_sale_expense/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('waaneiza_sale_expense.listing', {
#             'root': '/waaneiza_sale_expense/waaneiza_sale_expense',
#             'objects': http.request.env['waaneiza_sale_expense.waaneiza_sale_expense'].search([]),
#         })

#     @http.route('/waaneiza_sale_expense/waaneiza_sale_expense/objects/<model("waaneiza_sale_expense.waaneiza_sale_expense"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('waaneiza_sale_expense.object', {
#             'object': obj
#         })

