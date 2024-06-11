from odoo import fields, models, api, _


class ResCurrencyRateExt(models.Model):
    _inherit = 'res.currency.rate'

    @api.depends('rate', 'name', 'currency_id', 'company_id', 'currency_id.rate_ids.rate')
    @api.depends_context('company')
    def _compute_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.company_rate = round((currency_rate.rate or currency_rate._get_latest_rate().rate or 1.0) / last_rate[company],5)
        else:
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.company_rate = (currency_rate.rate or currency_rate._get_latest_rate().rate or 1.0) / \
                                             last_rate[company]

    @api.onchange('company_rate')
    def _inverse_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.rate = round(currency_rate.company_rate * last_rate[company],5)
        else:
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.company_rate = (currency_rate.rate or currency_rate._get_latest_rate().rate or 1.0) / \
                                             last_rate[company]

    @api.depends('company_rate')
    def _compute_inverse_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            for currency_rate in self:
                if not currency_rate.company_rate:
                    currency_rate.company_rate = 1.0
                currency_rate.inverse_company_rate = round(1.0 / currency_rate.company_rate,5)
        else:
            for currency_rate in self:
                if not currency_rate.company_rate:
                    currency_rate.company_rate = 1.0
                currency_rate.inverse_company_rate = 1.0 / currency_rate.company_rate


    @api.onchange('inverse_company_rate')
    def _inverse_inverse_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            for currency_rate in self:
                if not currency_rate.inverse_company_rate:
                    currency_rate.inverse_company_rate = 1.0
                currency_rate.company_rate = round(1.0 / currency_rate.inverse_company_rate,5)
        else:
            for currency_rate in self:
                if not currency_rate.inverse_company_rate:
                    currency_rate.inverse_company_rate = 1.0
                currency_rate.company_rate = 1.0 / currency_rate.inverse_company_rate

    @api.onchange('company_rate')
    def _onchange_rate_warning(self):
        # We send the ETA a rate that is 5 decimal accuracy, so to ensure consistency, Odoo should also operate with 5 decimal accuracy rate
        if self.company_id.account_fiscal_country_id.code == 'EG' and self.inverse_company_rate != round(
                self.inverse_company_rate, 5):
            return {
                'warning': {
                    'title': _("Warning for %s", self.currency_id.name),
                    'message': _(
                        "Please make sure that the EGP per unit is within 5 decimal accuracy.\n"
                        "Higher decimal accuracy might lead to inconsistency with the ETA invoicing portal!"
                    )
                }
            }
        return super()._onchange_rate_warning()

