from odoo import models, fields, api
from odoo import _


class Disease(models.Model):
    """
    Model representing a disease entity within the hospital system.

    This model supports hierarchical disease classifications and
    allows for categorization under different disease types. It can
    also maintain parent-child relationships between diseases.

    Fields:
        - name (Char): Name of the disease.
        - complete_name (Char): Full hierarchical name of the disease,
        including parent names.
        - description (Text): Description or details about the disease.
        - parent_id (Many2one): Reference to the parent disease.
        - child_ids (One2many): List of child diseases associated with
        the current disease.
        - disease_type_id (Many2one): Reference to the type of disease.
    """
    _name = 'a_hospital.disease'
    _description = 'Hospital Disease'
    _parent_store = True                # Вкл. підтримку ієрархії
    _parent_name = "parent_id"
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string="Disease Name", required=True)

    complete_name = fields.Char(
        compute='_compute_complete_name',
        recursive=True,
        store=True)

    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name='a_hospital.disease',
        string='Parent Disease',
        ondelete='cascade',
    )

    child_ids = fields.One2many(
        comodel_name='a_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )

    parent_path = fields.Char(
        index=True,
        unaccent=False)

    disease_type_id = fields.Many2one(
        comodel_name='a_hospital.disease.type',
        string='Disease Type',
        required=False
    )

    @api.constrains('parent_id')
    def _check_parent_id(self):
        """
        Prevents the creation of cyclic disease hierarchies.
        Raises:
            ValidationError: If a recursive hierarchy is detected.
        """
        if not self._check_recursion():
            raise models.ValidationError(_(
                'You cannot create recursive hierarchy.'))

    @api.depends('name', 'parent_id')
    def _compute_complete_name(self):
        """
        Generates a complete hierarchical name for the disease,
        combining parent and child names.
        """
        for disease in self:
            if disease.parent_id:
                disease.complete_name = '%s / %s' % (
                    disease.parent_id.complete_name,
                    disease.name)
            else:
                disease.complete_name = disease.name
