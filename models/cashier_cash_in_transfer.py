# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CashirCashInTransfer(models.Model):
    _name = 'cashier.cash.in.transfer'
    _inherit = ['cashier.cash.in.transfer', 'utm.mixin']

    cash_sale_id = fields.Many2one('account.move',string='Sale Order')
    e_id = fields.Integer()
    sale_transfer=fields.Boolean(default="No")

    # def action_confirm_sale(self):
    #     self.state = "confirm"
    def action_confirm(self):
        self.state = "confirm"
        self.sale_transfer="Yes"
        self.cash_sale_id.m_type='done'
    def action_done(self):
        self.state='done'
        self.cash_sale_id.state = 'transfer'
        self.cash_sale_id.payment_state = 'paid'

    @api.onchange('cash_sale_id')           
    def _onchange_sale_cashir(self):
         for rec in self:
            if rec.cash_sale_id.id > 0:
                rec.e_id=rec.cash_sale_id.emp_id_info
                rec.type = "process"
                rec.datetime = rec.cash_sale_id.invoice_date
                rec.company_id = rec.cash_sale_id.company_id.id
                rec.type_of_code = "SCI"
                rec.currency = rec.cash_sale_id.currency_id.id
                rec.type_of_transfer = rec.cash_sale_id.type_cashier_transfer
                rec.bank_name_test = rec.cash_sale_id.bank_name_cashier.id
                rec.bank_account_test = rec.cash_sale_id.bank_account_cashier.id
                rec.total_amount = rec.cash_sale_id.amount_total
                for line in rec.cash_sale_id:
                        rec.cash_in_transfer_lines = [(0,0,{
                        'sr_no':'1',
                        'datetime':rec.cash_sale_id.invoice_date,
                        'vr_no':rec.cash_sale_id.invoice_origin,
                        'code':rec.cash_sale_id.invoice_origin,
                        'remarks':'Sale Transfer',
                        'amount':rec.cash_sale_id.amount_total
                    })]
                rec.transfered_by_name = rec.e_id
    
            else:
                pass