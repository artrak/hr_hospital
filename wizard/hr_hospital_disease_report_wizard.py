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
        self.ensure_one()
        domain = [('visit_id.visit_date', '>=', self.date_from),
                  ('visit_id.visit_date', '<=', self.date_to)]

        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        diagnoses = self.env['hr_hospital.diagnosis'].search(domain)
        action = self.env.ref(
            'hr_hospital.action_hr_hospital_diagnosis').read()[0]
        action['domain'] = [('id', 'in', diagnoses.ids)]
        return action
