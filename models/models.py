# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class report_xlsx_partner_debt(models.Model):
#     _name = 'report_xlsx_partner_debt.report_xlsx_partner_debt'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class report_xlsx_partner_debt(models.Model):
    _name = 'account.payment'
    _inherit = 'account.payment'

    previous_period = fields.Boolean(string="Previous Period Payment",default=False)
