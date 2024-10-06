from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _inherit = 'hr_hospital.person'
    _name = 'hr_hospital.patient'
    _description = 'Patient'

    personal_doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string="Personal Doctor",
    )

    birth_date = fields.Date(string="Date of Birth")

    passport_details = fields.Char()

    contact_person = fields.Char(string="Emergency Contact")

    age = fields.Integer(
        compute='_compute_age',
        store=True,
    )

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Disease')

    doctor_id = fields.Many2one(
        'hr_hospital.doctor',
        string='Person doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = relativedelta(
                    fields.Date.today(),
                    record.birth_date).years
            else:
                record.age = 0

    # loging for create
    @api.model
    def create(self, vals):
        patient = super(Patient, self).create(vals)
        _logger.info(f"New patient created: "
                     f"{patient.first_name} {patient.last_name}, "
                     f"ID: {patient.id}")
        return patient

    # loging for write
    def write(self, vals):
        result = super(Patient, self).write(vals)
        _logger.info(f"Patient updated: "
                     f"{self.first_name} {self.last_name}, "
                     f"ID: {self.id}")
        return result
