from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = 'a_hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    personal_doctor_id = fields.Many2one(
        comodel_name='a_hospital.doctor',
        string='Personal doctor'
    )

    def change_personal_doctor(self):
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids')
        for active_id in active_ids:
            patient = self.env[active_model].browse(active_id)
            patient.doctor_id = self.personal_doctor_id
