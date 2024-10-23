# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class waaneiza_sale_expense(models.Model):
#     _name = 'waaneiza_sale_expense.waaneiza_sale_expense'
#     _description = 'waaneiza_sale_expense.waaneiza_sale_expense'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

