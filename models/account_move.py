# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'utm.mixin']

    sale_code_integer= fields.Integer()
    sale_order_code= fields.Char(string="Sale Order Code")
    emp_id = fields.Integer(compute='_onchange_user_id')
    emp_id_info = fields.Integer(compute='_onchange_emp_id')
    bank_integer = fields.Integer(compute='_onchange_bank_id')
    move_type = fields.Selection(selection_add=[('cash in transfer', 'Cash In Transfer')],ondelete={'cash in transfer': 'set default'})
    payment_state = fields.Selection(selection_add=[('transfer', 'Cash In Transfer')], ondelete={'transfer': 'cascade'})
    m_type = fields.Selection([
        ('not transfer', 'Not Transfer'),
        ('transfer', 'Transfer'),
        ('done','Done')
    ], string='Type of Transfer', index=True, store=True, default='not transfer')
    sale_cashin_transfer_lines = fields.One2many('cashier.cash.in.transfer','cash_sale_id',string="Cashin Transfer Line", index=True, copy=False, store=True, readonly=False)
    
    def comput_sale_order_code(self):
        self.sale_code_integer = self.invoice_line_ids.mapped('sale_line_ids').order_id
        self.env.cr.execute("""select name from sale_order
                                where id=%s""" % (self.sale_code_integer))
        res = self.env.cr.fetchone()
        self.sale_order_code = res and res[0]

    def create_cash_transfer(self):
        self.sale_code_integer = self.invoice_line_ids.mapped('sale_line_ids').order_id
        # bank_name = self.partner_bank_id.bank_id
        # bank_integer=self.partner_bank_id.id
        self.env.cr.execute("""select name from sale_order
                                where id=%s""" % (self.sale_code_integer))
        res = self.env.cr.fetchone()
        sale_order_code = res and res[0]
        inv_obj = self.env['cashier.cash.in.transfer']
        self.ensure_one()
        invoice = inv_obj.create({
            'type':'process',
            'datetime': self.invoice_date,
            'company_id':self.company_id.id,
            'type_of_code': 'SCI',
            'currency':self.currency_id.id,
            'type_of_transfer':self.type_cashier_transfer,
            'bank_name_test':self.bank_name_cashier.id,
            'bank_account_test':self.bank_account_cashier.id,
            'total_amount': self.amount_total,
            'cash_in_transfer_lines':[(0,0,{
                'sr_no':self.sale_code_integer,
                'datetime':self.invoice_date,
                'vr_no':sale_order_code,
                'code':sale_order_code,
                'remarks':'Sale Transfer',
                'amount':self.amount_total,

                })],
            'transfered_by_name':self.emp_id_info,
            })
        self.m_type='transfer'
        self.state = 'transfer'
        self.payment_state = 'paid'

    @api.depends('invoice_user_id')
    def _onchange_user_id(self):
        if  self.invoice_user_id.id >= 1:
            self.env.cr.execute("""select id from hr_employee
                                where hr_employee.user_id=%s""" % (self.invoice_user_id.id))
            res = self.env.cr.fetchone()
            self.emp_id = res and res[0]
        else:
             self.emp_id = 1
    @api.depends('emp_id')
    def _onchange_emp_id(self):
        if  self.emp_id >= 1:
            self.env.cr.execute("""select emp_info_ids from hr_employee
                                where id=%s""" % (self.emp_id))
            res = self.env.cr.fetchone()
            self.emp_id_info = res and res[0]
        else:
            self.emp_id_info = 1

    @api.depends('partner_bank_id')
    def _onchange_bank_id(self):
        if self.partner_bank_id.id >= 1:
            self.env.cr.execute("""select bank_id from res_partner_bank
                                where id=%s""" % (self.partner_bank_id.id))
            res = self.env.cr.fetchone()
            self.bank_integer = res and res[0]
        else:
            self.bank_integer=1

    def create_sale_cashtransfer(self):
        return {
            'res_model': 'cashier.cash.in.transfer',
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_expense_cashier.cashier_cash_in_transfer_form").id,
            'target': 'self.'
        }
    transfer_count = fields.Integer(compute="_compute_transfer_count", string='Transfer Counts', copy=False, default=0, store=True)
    transfer_ids = fields.Many2many('cashier.cash.in.transfer', compute="_compute_transfer_count", string='CashTransfer', copy=False, store=True)
    
    @api.depends('sale_cashin_transfer_lines')
    def _compute_transfer_count(self):
        for count in self:
            counts = count.mapped('sale_cashin_transfer_lines')
            count.transfer_ids = counts
            count.transfer_count = len(counts)

    def action_view_cash_transfer(self, counts=False, context=None):
        if not counts:
            counts = self.transfer_ids
        if len(counts) > 1:
            result = self.env['ir.actions.act_window']._for_xml_id('waaneiza_expense_cashier.action_cashier_cash_in_transfer')
            result['domain'] = [('id', 'in', counts.ids)]
            return result

        elif len(counts) == 1:
            return {
            'res_model': 'cashier.cash.in.transfer',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_expense_cashier.cashier_cash_in_transfer_form").id,
            'target': 'self.',
            'res_id': counts.id
        }

        
