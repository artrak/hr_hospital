from odoo import models, fields


class DiseaseType(models.Model):
    """
    Model representing a category or type of disease in the hospital system.

    DiseaseType is used for classifying diseases into different types,
    aiding in organized disease management within the system.

    Fields:
        - name (Char): The name of the disease type.
        - description (Text): Description of the disease type.
        - disease_ids (One2many): List of diseases categorized under this type.
    """
    _name = 'a_hospital.disease.type'
    _description = 'Disease Type'

    name = fields.Char(string="Type Name", required=True)
    description = fields.Text()

    disease_ids = fields.One2many(
        comodel_name='a_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )
