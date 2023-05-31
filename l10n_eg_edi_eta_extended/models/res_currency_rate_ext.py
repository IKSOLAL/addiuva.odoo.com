from odoo import fields, models, api, _

class ResCurrencyRateExt(models.Model):
    _inherit = 'res.currency.rate'

    @api.onchange('company_rate')
    def _onchange_rate_warning(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            self.company_rate = round(self.company_rate,5)
            self.inverse_company_rate = round(self.inverse_company_rate,5)
        else:
            self.company_rate = self.company_rate
            self.inverse_company_rate = self.inverse_company_rate

    @api.depends('rate', 'name', 'currency_id', 'company_id', 'currency_id.rate_ids.rate')
    @api.depends_context('company')
    def _compute_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.company_rate = (currency_rate.rate or currency_rate._get_latest_rate().rate or 1.0) / \
                                             last_rate[
                                                 company]
                currency_rate.company_rate = round(currency_rate.company_rate, 5)
                currency_rate.inverse_company_rate = round(currency_rate.inverse_company_rate, 5)
        else:
            last_rate = self.env['res.currency.rate']._get_last_rates_for_companies(self.company_id | self.env.company)
            for currency_rate in self:
                company = currency_rate.company_id or self.env.company
                currency_rate.company_rate = (currency_rate.rate or currency_rate._get_latest_rate().rate or 1.0) / \
                                             last_rate[
                                                 company]
                currency_rate.company_rate = currency_rate.company_rate
                currency_rate.inverse_company_rate = currency_rate.inverse_company_rate

    @api.depends('company_rate')
    def _compute_inverse_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            for currency_rate in self:
                if currency_rate.company_rate>0:
                    currency_rate.inverse_company_rate = 1.0 / currency_rate.company_rate
        else:
            for currency_rate in self:
                if currency_rate.company_rate>0:
                    currency_rate.inverse_company_rate = 1.0 / currency_rate.company_rate

    @api.onchange('inverse_company_rate')
    def _inverse_inverse_company_rate(self):
        if self.company_id.account_fiscal_country_id.code == 'EG':
            for currency_rate in self:
                currency_rate.company_rate = 1.0 / currency_rate.inverse_company_rate
                currency_rate.company_rate = round(currency_rate.company_rate,5)
        else:
            for currency_rate in self:
                if currency_rate.inverse_company_rate > 0:
                    currency_rate.company_rate = 1.0 / currency_rate.inverse_company_rate