from odoo import models, fields

class Visit(models.Model):
    _name = 'hr_hospital2.visit'
    _description = 'Patient Visit'

    patient_id = fields.Many2one('hr_hospital2.patient', string='Patient', required=True)
    doctor_id = fields.Many2one('hr_hospital2.doctor', string='Doctor', required=True)
    visit_date = fields.Date(string='Visit Date', required=True)
    notes = fields.Text(string='Notes')
