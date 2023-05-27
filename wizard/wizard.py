from odoo import models, fields, api

class PartnerDebt(models.TransientModel):
    _name = 'account.debt.report'

    partner = fields.Many2one('res.partner',
        string="Partner", required=True)
    start_date = fields.Date(string="From")
    end_date = fields.Date(strinh="To")

    
    def export_xlsx(self):
        module = __name__.split('addons.')[1].split('.')[0]
        report_name = '{}.partner_debt_xlsx'.format(module)
        data = {}
        data['form'] = self.read(['partner', 'start_date', 'end_date'])[0]
        data['dynamic_report'] = True
        report = {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'report_name': report_name,
            # model name will be used if no report_file passed via context
            'context': dict(self.env.context, report_file='partner'),
            # report_xlsx doesn't pass the context if the data dict is empty
            # cf. report_xlsx\static\src\js\report\qwebactionmanager.js
            # TODO: create PR on report_xlsx to fix this
            'data': data,
        }
        return report
