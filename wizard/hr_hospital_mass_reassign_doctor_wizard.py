from odoo import fields, models, api
from odoo.exceptions import UserError


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr_hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    doctor_id = fields.Many2one('hr_hospital.doctor', string="New Personal Doctor", required=True)
    patient_ids = fields.Many2many('hr_hospital.patient', string="Patients")

    def action_reassign_doctor(self):
        self.ensure_one()
        if not self.patient_ids:
            raise UserError("Please select at least one patient.")
        for patient in self.patient_ids:
            patient.personal_doctor_id = self.doctor_id
