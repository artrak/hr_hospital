from odoo import models, fields, api


class Person(models.AbstractModel):
    _name = 'hr_hospital.person'
    _description = 'Person'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last name', required=True)
    phone = fields.Char(string='Phone')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender',
        required=True,
    )
    photo = fields.Image(
        string='Photo',
        max_width=512,
        max_height=512,
    )

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.first_name} {record.last_name}"

