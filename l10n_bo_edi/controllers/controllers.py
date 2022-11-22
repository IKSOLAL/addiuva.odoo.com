# -*- coding: utf-8 -*-
# from odoo import http


# class L10nBoEdi(http.Controller):
#     @http.route('/l10n_bo_edi/l10n_bo_edi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_bo_edi/l10n_bo_edi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_bo_edi.listing', {
#             'root': '/l10n_bo_edi/l10n_bo_edi',
#             'objects': http.request.env['l10n_bo_edi.l10n_bo_edi'].search([]),
#         })

#     @http.route('/l10n_bo_edi/l10n_bo_edi/objects/<model("l10n_bo_edi.l10n_bo_edi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_bo_edi.object', {
#             'object': obj
#         })
