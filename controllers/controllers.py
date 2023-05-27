# -*- coding: utf-8 -*-
from odoo import http

# class ReportXlsxPartnerDebt(http.Controller):
#     @http.route('/report_xlsx_partner_debt/report_xlsx_partner_debt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_xlsx_partner_debt/report_xlsx_partner_debt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_xlsx_partner_debt.listing', {
#             'root': '/report_xlsx_partner_debt/report_xlsx_partner_debt',
#             'objects': http.request.env['report_xlsx_partner_debt.report_xlsx_partner_debt'].search([]),
#         })

#     @http.route('/report_xlsx_partner_debt/report_xlsx_partner_debt/objects/<model("report_xlsx_partner_debt.report_xlsx_partner_debt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_xlsx_partner_debt.object', {
#             'object': obj
#         })