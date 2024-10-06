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

    disease_id = fields.Many2one(
        comodel_name='hr_hospital.disease',
        string='Disease',
        required=True
    )

    # name = fields.Char(
    #     string='Diagnosis Name',
    #     related="disease_id.name"
    # )

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
