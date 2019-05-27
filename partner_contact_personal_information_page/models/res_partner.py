# Copyright <2019> <BerrySoft MX>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.utils import formataddr

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit="res.partner"

    personal_street = fields.Char()
    personal_street2 = fields.Char()
    personal_zip = fields.Char(change_default=True)
    personal_city = fields.Char()
    personal_state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', personal_country_id)]")
    personal_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    personal_email = fields.Char()
    personal_email_formatted = fields.Char(
        'Formatted Email', compute='_compute_email_formatted',
        help='Format email address "Name <email@domain>"')
    personal_phone = fields.Char()
    personal_mobile = fields.Char()

    @api.onchange('personal_country_id')
    def _onchange_personal_country_id(self):
        if self.personal_country_id and self.personal_country_id != self.personal_state_id.country_id:
            self.personal_state_id = False

    @api.onchange('personal_state_id')
    def _onchange_personal_state(self):
        if self.personal_state_id.country_id:
            self.personal_country_id = self.personal_state_id.country_id

    @api.onchange('personal_email')
    def onchange_personal_email(self):
        if not self.image and self._context.get('gravatar_image') and self.personal_email:
            self.image = self._get_gravatar_image(self.personal_email)

    @api.depends('personal_name', 'personal_email')
    def _compute_personal_email_formatted(self):
        for partner in self:
            if partner.personal_email:
                partner.personal_email_formatted = formataddr((partner.name or u"False", partner.personal_email or u"False"))
            else:
                partner.personal_email_formatted = ''
