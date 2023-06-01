from odoo import api, fields, models, _


class EdiMxCancelMotive(models.Model):
    _name = 'cancel.motive'
    _description = 'Motivo de cancelacion'
    _rec_name = 'name'
    
    name = fields.Char(
        string='Motivo cancelación',
    )
    default_code = fields.Char(
        string='Código',
    )
    is_to_payment = fields.Boolean(
        string='Es para pago',
    )

