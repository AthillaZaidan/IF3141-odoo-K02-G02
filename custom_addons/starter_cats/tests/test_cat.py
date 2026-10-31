from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestCat(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        group_user = cls.env.ref("starter_cats.group_cat_user")
        cls.user_a = cls.env["res.users"].create(
            {"name": "Cat User A", "login": "cat_a", "groups_id": [(6, 0, [group_user.id])]}
        )
        cls.user_b = cls.env["res.users"].create(
            {"name": "Cat User B", "login": "cat_b", "groups_id": [(6, 0, [group_user.id])]}
        )
        cls.cat = cls.env["starter.cat"].create({"name": "Tom"})

    def test_valid_transitions(self):
        self.cat.action_activate()
        self.assertEqual(self.cat.state, "active")
        self.cat.action_set_archived()
        self.assertEqual(self.cat.state, "archived")

    def test_invalid_transitions(self):
        # draft tidak boleh langsung ke archived
        with self.assertRaises(UserError):
            self.cat.action_set_archived()
        self.cat.action_activate()
        # active tidak boleh diaktifkan lagi
        with self.assertRaises(UserError):
            self.cat.action_activate()

    def test_birth_date_in_future(self):
        tomorrow = fields.Date.context_today(self.cat) + timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.cat.birth_date = tomorrow

    def test_user_cannot_read_other_users_cat(self):
        cat_a = self.env["starter.cat"].with_user(self.user_a).create({"name": "Mine"})
        self.assertEqual(cat_a.name, "Mine")
        with self.assertRaises(AccessError):
            cat_a.with_user(self.user_b).read(["name"])
