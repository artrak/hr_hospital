from odoo import models, fields, api
from odoo import _


class Disease(models.Model):
    _name = 'hr_hospital.disease'
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
        comodel_name='hr_hospital.disease',
        string='Parent Disease',
        ondelete='cascade',
    )

    child_ids = fields.One2many(
        comodel_name='hr_hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )

    parent_path = fields.Char(
        index=True,
        unaccent=False)

    disease_type_id = fields.Many2one(
        comodel_name='hr_hospital.disease.type',
        string='Disease Type',
        required=False
    )

    @api.constrains('parent_id')        # захист від циклічних посилань
    def _check_parent_id(self):
        if not self._check_recursion():
            raise models.ValidationError(_(
                'You cannot create recursive hierarchy.'))

    # збираємо complete_name
    @api.depends('name', 'parent_id')
    def _compute_complete_name(self):
        for disease in self:
            if disease.parent_id:
                disease.complete_name = '%s / %s' % (
                    disease.parent_id.complete_name,
                    disease.name)
            else:
                disease.complete_name = disease.name
