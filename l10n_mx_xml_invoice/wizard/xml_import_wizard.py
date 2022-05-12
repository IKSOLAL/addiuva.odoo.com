from odoo import fields, models, _
from odoo.exceptions import UserError


class XmlImportWizard(models.TransientModel):
    _name = 'xml.import.wizard'
    _description = 'For import wizard'

    xml_import_invoice_id = fields.Many2one(
        comodel_name="xml.import.invoice",
        string="Xml invoice",
        required=True,
    )
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        string='Files',
        required=True,
    )

    def import_xml(self):
        for data_file in self.attachment_ids:
            print(data_file.name[-4:])
            if data_file.name[-4:] == '.xml':
                self.xml_import_invoice_id.write({
                    'xml_table_ids': [(0, None, {
                        'xml': data_file.datas
                    })]
                })
            else:
                raise UserError(
                    _('File %s is not xml type, please remove from list')
                    % (data_file.display_name)
                )
        if self.attachment_ids:
            self.xml_import_invoice_id.validate_xml()
        return True
