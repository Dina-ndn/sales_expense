from odoo import models, fields, api, exceptions, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    warehouse_id_testing=fields.Char(string="Warehouse")
    emp_id = fields.Integer(compute='_onchange_user_id')
    emp_id_info = fields.Integer(compute='_onchange_emp_id')

    def create_cash_transfer(self):
        inv_obj = self.env['cashier.cash.in.transfer']
        self.ensure_one()
        invoice = inv_obj.create({
            'type':'process',
            'datetime': self.date_order,
            'company_id':self.company_id.id,
            'type_of_code': 'SCI',
            'currency':self.currency_id.id,
            'type_of_transfer':'bank',
            'total_amount': self.amount_total,
            'cash_in_transfer_lines':[(0,0,{
                'sr_no':1,
                'datetime':self.date_order,
                # 'datetime':'2020-01-10',
                'vr_no':self.name,
                'code':self.name,
                'remarks':'Sale Transfer',
                'amount':self.amount_total,

                })],
            'transfered_by_name':self.emp_id_info,
            })

        # inv_obj = self.env['se.apple']
        # self.ensure_one()
        # invoice = inv_obj.create({
        #     'apple_name': 'Testing',
        #     'apple_description': 'Testing Description',
        #     'apple_remarks': 'Testing Remark',
        # })

    @api.depends('user_id')
    def _onchange_user_id(self):
        # self.env.cr.execute("""select id from hr_employee
        #                         where user_id=%s""" % (self.user_id))
        # res = self.env.cr.fetchone()
        # self.emp_id = res and res[0]
        self.env.cr.execute("""select id from hr_employee
                                where hr_employee.user_id=%s""" % (self.user_id.id))
        res = self.env.cr.fetchone()
        self.emp_id = res and res[0]

    @api.depends('emp_id')
    def _onchange_emp_id(self):
        self.env.cr.execute("""select emp_info_ids from hr_employee
                                where id=%s""" % (self.emp_id))
        res = self.env.cr.fetchone()
        self.emp_id_info = res and res[0]

    def action_cash_transfer(self):
        return {
            'res_model': 'cashier.cash.in.transfer',
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref("waaneiza_expense_cashier.cashier_cash_in_transfer_form").id,
            'target': 'self.'
        }

