# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_driver = fields.Boolean('Driver')


class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    vehicle_type = fields.Selection([('Vehicle', 'Vehicle'), ('Trailer', 'Trailer')], 'Type')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    from_id = fields.Many2one("res.partner")
    to_id = fields.Many2one("res.partner")
    departure_time = fields.Datetime()
    arrival_time = fields.Datetime()
    transportation_ids = fields.One2many('transportation.operation', 'sale_id', string='Transfers')

    # def action_view_delivery2(self):
    #     '''
    #     This function returns an action that display existing delivery orders
    #     of given sales order ids. It can either be a in a list or in a form
    #     view, if there is only one delivery order to show.
    #     '''
    #     action = self.env.ref('telenoc_transportation.transportation_operation_all_action').read()[0]
    #
    #     pickings = self.mapped('transportation_ids')
    #     if len(pickings) > 1:
    #         action['domain'] = [('id', 'in', pickings.ids)]
    #     elif pickings:
    #         form_view = [(self.env.ref('telenoc_transportation.transportation_operation_form').id, 'form')]
    #         if 'views' in action:
    #             action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
    #         else:
    #             action['views'] = form_view
    #         action['res_id'] = pickings.id
    #     # Prepare the context.
    #     # picking_id = pickings.filtered(lambda l: l.picking_type_id.code == 'outgoing')
    #     # if picking_id:
    #     #     picking_id = picking_id[0]
    #     # else:
    #     #     picking_id = pickings[0]
    #     action['context'] = dict(self._context, default_sale_id=self.id, default_from_id=self.from_id.id,
    #                              default_to_id=self.to_id.id,
    #                              default_departure_time=self.departure_time,
    #                              default_arrival_time=self.arrival_time,
    #                              )
    #     return action

    def action_view_transportation(self):
        transportation_id = self.env['transportation.operation']
        transportation_obj = transportation_id.search([('sale_id', '=', self.id)])
        if transportation_obj:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Transportation',
                'res_model': 'transportation.operation',
                'res_id': transportation_obj.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            transportation_obj = transportation_id.create({
                    'sale_id': self.id,
                    'from_id': self.from_id.id,
                    'to_id': self.to_id.id,
                    'departure_time': self.departure_time,
                    'arrival_time': self.arrival_time,
                })
            for record in self.order_line:
                res = {
                        'transportation_product_id': transportation_obj.id,
                        'product_id': record.product_id.id,
                        'quantity': record.product_uom_qty,
                    }
                transportation_obj.update({
                    'product_ids': [(0, 0, res)],
                })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Transportation',
                'res_model': 'transportation.operation',
                'res_id': transportation_obj.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'current',
            }

# class QualityCheck(models.Model):
#     _inherit = "quality.check"
#
#     mrp_production_id = fields.Many2one(comodel_name="mrp.production")
#     test_line_ids = fields.One2many("quality.test.lines", "quality_test_id")
#     analyzed_by_id = fields.Many2one("res.users")
#     start_date = fields.Datetime()
#     end_date = fields.Datetime()
#     no_of_sterility = fields.Float()
#     no_of_colonies = fields.Float()
#     is_pass = fields.Boolean(compute='get_pass_value', default=False, store=True)
#
#     @api.onchange('product_id')
#     def _onchange_product_id(self):
#         if self.product_id:
#             if self.test_line_ids:
#                 self.test_line_ids=False
#             old_lines = self.env['quality.check.test'].search([('product_id', '=', self.product_id.id)])
#             if old_lines:
#                 for record in old_lines:
#                     for line in record.quality_test_ids:
#                         res = {
#                                 # 'quality_test_id': self.id,
#                                 'question_id': line.question_id.id,
#                                 'question_type': line.question_type,
#                                 'q_from': line.q_from,
#                                 'q_to': line.q_to,
#                                 'specification': line.specification,
#                                 'is_success': line.is_success,
#                             }
#                         self.update({
#                             'test_line_ids': [(0, 0, res)],
#                         })
#                         # new_lines.new(res)
#
#     @api.depends('test_line_ids')
#     def get_pass_value(self):
#         for record in self:
#             for line in record.test_line_ids:
#                 if line.is_success == False:
#                     record.is_pass = False
#                     break
#                 else:
#                     record.is_pass = True
#
#     def do_pass(self):
#         if self.is_pass == False:
#             raise UserError(_("Please review your Quality Tests result"))
#         res = super(QualityCheck, self).do_pass()
#         self.mrp_production_id.button_mark_done()
#         return res


# class MrpProduction(models.Model):
#     _inherit = "mrp.production"
#
#     state = fields.Selection(selection_add=[('test', 'Testing')])
# #     state = fields.Selection([
# #         ('confirmed', 'Confirmed'),
# #         ('planned', 'Planned'),
# #         ('progress', 'In Progress'),
# #         ('test', 'Testing'),
# #         ('done', 'Done'),
# #         ('cancel', 'Cancelled')], string='State',
# #         copy=False, default='confirmed', track_visibility='onchange')
#
#     # @api.multi
#     def button_check_testing(self):
#         team_id = self.env['quality.alert.team'].search([])[0]
#         qc_id = self.env['quality.check'].create(
#             {
#                 'product_id': self.product_id.id,
#                 'mrp_production_id': self.id,
#                 'team_id': team_id.id,
#             }
#         )
#         qc_id.test_line_ids = {}
#         old_lines = self.env['quality.check.test'].search([('product_id', '=', self.product_id.id)])
#         new_lines = self.env['quality.test.lines']
#         if old_lines:
#             for record in old_lines:
#                 for line in record.quality_test_ids:
#                     res = {
#                             'quality_test_id': qc_id.id,
#                             'question_id': line.question_id.id,
#                             'question_type': line.question_type,
#                             'q_from': line.q_from,
#                             'q_to': line.q_to,
#                             'specification': line.specification,
#                         }
#                     new_lines.create(res)
#         self.write({'state': 'test'})

