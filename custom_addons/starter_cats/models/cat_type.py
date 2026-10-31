from odoo import fields, models


class StarterCatType(models.Model):
    _name = "starter.cat.type"
    _description = "Cat Type"
    _order = "name"

    name = fields.Char(required=True)

    # Constraint di level database; nama unik per jenis kucing.
    _sql_constraints = [
        ("name_uniq", "unique(name)", "Cat type name must be unique."),
    ]
