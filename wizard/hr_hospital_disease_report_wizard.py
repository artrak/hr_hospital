from odoo import fields, models


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr_hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        'hr_hospital.doctor',
        string="Doctors")
    disease_ids = fields.Many2many(
        'hr_hospital.disease',
        string="Diseases")
    date_from = fields.Date(string="From", required=True)
    date_to = fields.Date(string="To", required=True)

    def action_generate_report(self):
        doctor_ids = self.doctor_ids.ids
        disease_ids = self.disease_ids.ids

        if not doctor_ids:
            doctor_ids = self.env['hr_hospital.doctor'].search([]).ids

        if not disease_ids:
            disease_ids = self.env['hr_hospital.disease'].search([]).ids

        return {
            'type': 'ir.actions.act_window',
            'name': 'List diseases',
            'res_model': 'hr_hospital.diagnosis',
            'target': 'new',
            'view_mode': 'list',
            'view_type': 'form',
            'domain': [
                ["doctor_id", "in", doctor_ids],
                ["disease_id", "in", disease_ids],
                ["create_date", ">", self.date_from],
                ["create_date", "<", self.date_to]
            ],
            'context': {'group_by': 'disease_id'},
        }
