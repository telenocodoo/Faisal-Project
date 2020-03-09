# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="P.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Char(string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Char(string="Shipping line")
    landing_place = fields.Char()
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status")

    def get_line_with_vat(self):
        total_with_vat = 0
        total_without_vat = 0
        for rec in self:
            for line in rec.invoice_line_ids:
                if line.tax_ids:
                    total_with_vat += line.price_subtotal
                else:
                    total_without_vat += line.price_subtotal
        vals= {'total_with_vat': total_with_vat ,'total_without_vat': total_without_vat,}
        return vals

class FmtOrderStatus(models.Model):
    _name = 'fmt.order.status'

    name = fields.Char(required=1)
