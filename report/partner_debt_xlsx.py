# -*- coding: utf-8 -*-
# Copyright 2009-2018 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PartnerDebtXlsx(models.AbstractModel):
    _name = 'report.report_xlsx_partner_debt.partner_debt_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def _get_ws_params(self, wb, data, acd):
#        partner = env['res.partner'].browse(data['form']['partner'][0])
#        sos = env['sale.report'].search([('confirmation_date','>',data['form']['start_date']),('date_invoice','<',data['form']['end_date']),
#            ('partner_id.id','=',data['form']['partner'][0])])
        order_template = {
            'so_code': {
                'header': {
                    'value': 'Code',
                },
                'data': {
                    'value': self._render("so.name"),
#self._render("data['form']['partner'].name"),
                },
                'width': 20,
            },
            'product': {
                'header': {
                    'value': 'Product',
                },
                'data': {
                    'value': self._render("so.product_id.name"),
                },
                'width': 20,
            },
            'quantity': {
                'header': {
                    'value': 'Quantity',
                },
                'data': {
                    'value': self._render("so.product_uom_qty"),
                },
                'width': 10,
            },
            'price_unit': {
                'header': {
                    'value': 'Price Unit',
                },
                'data': {
                    'value': self._render("so.product_id.lst_price"),
                },
                'width': 10,
            },
            'subtotal': {
                'header': {
                    'value': 'Subtotal',
                },
                'data': {
                    'type': 'formula',
                    'value': self._render("subtotal_formula"),
                },
                'width': 15,
            },
            'total': {
                'header': {
                    'value': 'Total',
                },
                'data': {
                    'type': 'formula',
                    'value': self._render("total_formula"),
                },
                'width': 15,
            },
        }


        order_wl = [
            'so_code','product','quantity','price_unit','subtotal','total']
        order_params = {
            'ws_name': 'Sale Order',
            'generate_ws_method': '_sale_report',
            'title': 'Sale Order',
            'wanted_list': order_wl,
            'col_specs': order_template,
        }
        purchase_params = {
            'ws_name': 'Purchase Order',
            'generate_ws_method': '_purchase_report',
            'title': 'Purchase Order',
            'wanted_list': order_wl,
            'col_specs': order_template,
        }
        payment_params = {
            'ws_name': 'Payment',
            'generate_ws_method': '_payment_report',
            'title': 'Payment',
            'wanted_list': order_wl,
            'col_specs': order_template,
        }
        debt_params = {
            'ws_name': 'Debt Report',
            'generate_ws_method': '_debt_report',
            'title': 'Debt Report',
            'wanted_list': order_wl,
            'col_specs': order_template,
        }

#        ws_params1 = {
#            'ws_name': 'Debt',
#            'generate_ws_method': '_partner_report',
#            'title': 'Partner',
#            'wanted_list': wanted_list,
#            'col_specs': partner_template,
#        }


        return [debt_params,order_params,payment_params,purchase_params]

    def _debt_report(self, wb, ws, debt_params, data, acd):

        ws.set_portrait()
        ws.fit_to_pages(1,0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, debt_params)

        row_pos = 0
        debt_params['title'] = data['form']['partner'][1]
        row_pos = self._write_ws_title(ws, row_pos, debt_params)

    def _payment_report(self, wb, ws, payment_params, data, acd):

        ws.set_portrait()
        ws.fit_to_pages(1,0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, payment_params)

        row_pos = 0
        payment_params['title'] = data['form']['partner'][1]
        row_pos = self._write_ws_title(ws, row_pos, payment_params)

    def _purchase_report(self, wb, ws, purchase_params, data, acd):

        ws.set_portrait()
        ws.fit_to_pages(1,0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, purchase_params)

        row_pos = 0
        purchase_params['title'] = data['form']['partner'][1]
        row_pos = self._write_ws_title(ws, row_pos, purchase_params)

    def _sale_report(self, wb, ws, order_params, data, acd):

#        partner = env['res.partner'].browse(data['form']['partner'][0])
        sos = self.env['sale.report'].search([('confirmation_date','>',data['form']['start_date']),('confirmation_date','<',data['form']['end_date']),
            ('partner_id.id','=',data['form']['partner'][0])])

        ws.set_portrait()
        ws.fit_to_pages(1,0)
        ws.set_header(self.xls_headers['standard'])
        ws.set_footer(self.xls_footers['standard'])

        self._set_column_width(ws, order_params)

        row_pos = 0
        order_params['title'] = data['form']['partner'][1]
        row_pos = self._write_ws_title(ws, row_pos, order_params)
        row_pos = self._write_line(
            ws, row_pos, order_params, col_specs_section='header',
            default_format=self.format_theader_yellow_left)
        ws.freeze_panes(row_pos, 0)

        wl = order_params['wanted_list']
        for so in sos:
            qty_cell = self._rowcol_to_cell(row_pos, wl.index('quantity'))
            price_cell = self._rowcol_to_cell(row_pos, wl.index('price_unit'))
            subtotal_formula = '{}*{}'.format(qty_cell,price_cell)

            total_formula = 'on_prog'
            row_pos = self._write_line(
                ws, row_pos, order_params, col_specs_section='data',
                render_space={
                    'so': so,
                    'subtotal_formula': subtotal_formula,
                    'total_formula': total_formula,
                },
                default_format=self.format_tcell_left)
#    def _partner_report(self, workbook, ws, ws_params, data, acd):

#        ws.set_portrait()
#        ws.fit_to_pages(1, 0)
#        ws.set_header(self.xls_headers['standard'])
#        ws.set_footer(self.xls_footers['standard'])

#       self._set_column_width(ws, ws_params)

#        row_pos = 0
#        ws_params['title'] = 'Que'
#        row_pos = self._write_ws_title(ws, row_pos, ws_params)
#        row_pos = self._write_line(
#            ws, row_pos, ws_params, col_specs_section='header',
#            default_format=self.format_theader_yellow_left)
#        ws.freeze_panes(row_pos, 0)

#        wl = ws_params['wanted_list']
#        for partner in ['Que']:
#            is_customer_pos = 'is_customer' in wl and \
#                wl.index('is_customer')
#            is_customer_cell = self._rowcol_to_cell(
#                row_pos, is_customer_pos)
#            customer_formula = 'IF({},"Y", "N")'.format(is_customer_cell)
#            row_pos = self._write_line(
#                ws, row_pos, ws_params, col_specs_section='data',
#                render_space={
#                },
#                default_format=self.format_tcell_left)

#    def generate_xlsx_report(self, workbook, data, objects):
#        super().generate_xlsx_report(self, workbook, data, objects)
#        sheet = workbook.add_worksheet('Report')
#        bold = workbook.add_format({'bold': True})
#        sheet.write(0, 0, str(, bold)
