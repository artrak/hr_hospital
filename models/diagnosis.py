from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import _


class Diagnosis(models.Model):
    _name = 'hr_hospital.diagnosis'
    _description = 'Diagnosis'

    visit_id = fields.Many2one(
        comodel_name='hr_hospital.visit',
        string='Visit',
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='hr_hospital.doctor',
        string='Doctor',
        required=True
    )

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Disease',
        required=True
    )

    patient_id = fields.Many2one(
        comodel_name='hr_hospital.patient',
        string='Patient',
        required=True,
    )

    description = fields.Text()

    is_approved = fields.Boolean(
        string='Approved',
        default=False,
        help="""This sign indicates that the given diagnosis,
                made by the mentor doctor,
                has been verified and approved by his mentor."""
    )

    doctor_approved = fields.Char(
        string='Doctor approved'
    )

    disease_type_id = fields.Many2one(
        related='disease_id.disease_type_id',
        comodel_name='hr_hospital.disease.type',
        string='Disease Type',
        store=True,
        readonly=True
    )

    # Перевіряємо, чи діагноз був зроблений інтерном,
    # і якщо так, вимагаємо підтвердження ментора
    @api.constrains('visit_id', 'is_approved')
    def _check_approval_for_intern(self):
        for diagnosis in self:
            doctor = diagnosis.visit_id.doctor_id
            if doctor.is_intern and diagnosis.is_approved:
                raise ValidationError(_(
                    "Diagnosis made by an intern must be approved "
                    "by the mentor."))

    # При створенні запису метод create перевіряє наявність visit_id у vals.
    # Якщо є, автоматично заповнює patient_id відповідним пацієнтом.
    @api.model
    def create(self, vals):
        if 'visit_id' in vals:
            visit = self.env['hr_hospital.visit'].browse(vals['visit_id'])
            vals['patient_id'] = visit.patient_id.id
        return super(Diagnosis, self).create(vals)

    # Користувач працює через інтерфейс і змінює значення visit_id,
    # тоді метод автоматично оновлює поле patient_id під час вибору візиту
    @api.onchange('visit_id')
    def _onchange_visit_id(self):
        for patient in self:
            patient.patient_id = patient.visit_id.patient_id
