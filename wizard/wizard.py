from odoo import models, fields, api
from datetime import datetime

class PartnerDebt(models.TransientModel):
    _name = 'account.debt.report'

    partner = fields.Many2one('res.partner',
        string="Partner", required=True)
    date_range = fields.Many2one('date.range',string="Period", default=lambda self: self._get_default_range())
    start_date = fields.Date(string="From", required=True)
    end_date = fields.Date(string="To", required=True)
    
    @api.model
    def _get_default_range(self):
        return self.env['date.range'].search([('name','=', datetime.today().strftime('%Y-%m'))])[0]

    @api.onchange('date_range')
    def _onchange_date_range(self):
        self.start_date = self.date_range.date_start
        self.end_date = self.date_range.date_end


    @api.multi
    def export_xlsx(self):
        module = __name__.split('addons.')[1].split('.')[0]
        report_name = '{}.partner_debt_xlsx'.format(module)
        data = {}
        data['form'] = self.read(['partner', 'start_date', 'end_date'])[0]
        data['dynamic_report'] = True
        file_name = data['form']['partner'][1].strip()
        file_name += " - "
        file_name += data['form']['start_date'].replace("-","")
        file_name += " - "
        file_name += data['form']['end_date'].replace("-","")        
        report = {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'report_name': report_name,
            # model name will be used if no report_file passed via context
            'context': dict(self.env.context, report_file=file_name),
            # report_xlsx doesn't pass the context if the data dict is empty
            # cf. report_xlsx\static\src\js\report\qwebactionmanager.js
            # TODO: create PR on report_xlsx to fix this
            'data': data,
        }
        return report
