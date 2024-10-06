from odoo import models, fields, api


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

        name = fields.Char(
            string='Diagnosis Name',
            required=True
        )

        description = fields.Text(string='Description')

        approved = fields.Boolean(
            string='Approved',
            default=False,
            # groups='base.group_system'
        )

