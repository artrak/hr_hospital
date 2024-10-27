from odoo import models, fields, api


class Person(models.AbstractModel):
    """
    Abstract model representing a basic person entity in the hospital system.

    Used as a base class for other models such as doctors and patients,
    providing common fields like name, phone, and gender.

    Fields:
        - first_name (Char): First name of the person.
        - last_name (Char): Last name of the person.
        - phone (Char): Phone number for contacting the person.
        - gender (Selection): Gender of the person, either male or female.
        - photo (Image): Profile photo of the person.
        - res_partner_id (Many2one): Reference to a contact entity
        in the system.
    """
    _name = 'a_hospital.person'
    _description = 'Person'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    phone = fields.Char()
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        required=True,
    )
    photo = fields.Image()

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Contact'
    )

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        """
        Computes a display name based on the first and last name of the person.
        """
        for record in self:
            record.display_name = \
                f"{record.first_name} {record.last_name}"
