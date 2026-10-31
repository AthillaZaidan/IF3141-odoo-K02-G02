from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class StarterCat(models.Model):
    _name = "starter.cat"
    _description = "Cat"
    # mail.thread menambahkan chatter dan tracking perubahan field.
    _inherit = ["mail.thread"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    cat_type_id = fields.Many2one("starter.cat.type", string="Type")
    birth_date = fields.Date()
    state = fields.Selection(
        [("draft", "Draft"), ("active", "Active"), ("archived", "Archived")],
        default="draft",
        required=True,
        tracking=True,
    )

    @api.constrains("birth_date")
    def _check_birth_date(self):
        today = fields.Date.context_today(self)
        for cat in self:
            if cat.birth_date and cat.birth_date > today:
                raise ValidationError(_("Birth date cannot be in the future."))

    # Guard transisi state: hanya draft -> active dan active -> archived.
    def _transition(self, source, target):
        for cat in self:
            if cat.state != source:
                raise UserError(
                    _(
                        "Cannot move '%(name)s' from %(src)s to %(dst)s.",
                        name=cat.name,
                        src=cat.state,
                        dst=target,
                    )
                )
        self.write({"state": target})

    def action_activate(self):
        self._transition("draft", "active")

    def action_set_archived(self):
        self._transition("active", "archived")
