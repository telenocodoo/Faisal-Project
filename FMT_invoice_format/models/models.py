# -*- coding: utf-8 -*-
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        invoice = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        account_move = self.env['account.move'].search([('invoice_origin', '=', sale_orders.name)])
        if account_move:
            print("rrrrrrrrrrr")
            account_move.update({
                'date_of_prealert': sale_orders.date_of_prealert,
                'eta_date': sale_orders.eta_date,
                'po_date': sale_orders.po_date,
                'saddad_payment_date': sale_orders.saddad_payment_date,
                'consinee': sale_orders.consinee.id,
                'bill_of_lading': sale_orders.bill_of_lading,
                'bayan': sale_orders.bayan,
                'shipping_line': sale_orders.shipping_line.id,
                'landing_place': sale_orders.landing_place.id,
                'order_status_id': sale_orders.order_status_id.id,
            })
        return invoice


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="D.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Many2one('sea.port')
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status", track_visibility='onchange')

    def action_view_invoice(self):
        res = super(SaleOrder, self).action_view_invoice()
        res['context'].update({
            'default_date_of_prealert': self.date_of_prealert,
            'default_eta_date': self.eta_date,
            'default_po_date': self.po_date,
            'default_saddad_payment_date': self.saddad_payment_date,
            'default_consinee': self.consinee.id,
            'default_bill_of_lading': self.bill_of_lading,
            'default_bayan': self.bayan,
            'default_shipping_line': self.shipping_line.id,
            'default_landing_place': self.landing_place.id,
            'default_order_status_id': self.order_status_id.id,
        })
        return res


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    arabic_name = fields.Char(related='product_id.arabic_name')


class AccountMove(models.Model):
    _inherit = 'account.move'

    date_of_prealert = fields.Date(string="Date of pre alert")
    eta_date = fields.Date(string="ETA")
    po_date = fields.Date(string="D.O Date")
    saddad_payment_date = fields.Date(string="Saddad Payment Date")
    consinee = fields.Many2one('consinee.sale.order', string="Consinee")
    bill_of_lading = fields.Char(string="Bill of Lading")
    bayan = fields.Char(string="Bayan")
    shipping_line = fields.Many2one('shipping.sale.order', string="Shipping line")
    landing_place = fields.Many2one('sea.port')
    order_status_id = fields.Many2one('fmt.order.status', string="Order Status", track_visibility='onchange')

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


class ConsineeSaleOrder(models.Model):
    _name = 'consinee.sale.order'

    name = fields.Char(required=1)


class ShippingSaleOrder(models.Model):
    _name = 'shipping.sale.order'

    name = fields.Char(required=1)


class SeaPort(models.Model):
    _name = 'sea.port'

    name = fields.Char(required=1)
    arabic_name = fields.Char(required=1)
