from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    document_type = fields.Selection(
        selection=[
            ("quotation", "報價單"),
            ("sales_order", "銷售訂單"),
            ("sales_slip", "銷貨單"),
        ],
        string="單據類型",
        default="quotation",
        tracking=True,
        required=True,
    )
    sales_slip_date = fields.Date(string="銷貨日期", default=fields.Date.context_today)
    sales_slip_contact = fields.Char(string="聯絡人")
    sales_slip_phone = fields.Char(string="聯絡電話")
    sales_slip_fax = fields.Char(string="傳真號碼")
    sales_slip_delivery_address = fields.Char(string="送貨地址")
    sales_slip_invoice_number_manual = fields.Char(string="手動發票號碼")
    sales_slip_invoice_number = fields.Char(
        string="發票號碼",
        compute="_compute_sales_slip_invoice_number",
        inverse="_inverse_sales_slip_invoice_number",
        store=True,
        readonly=False,
    )
    sales_slip_tax_type = fields.Selection(
        selection=[
            ("taxed", "應稅"),
            ("zero", "零稅率"),
            ("exempt", "免稅"),
        ],
        string="課稅別",
        default="taxed",
    )
    sales_slip_note = fields.Text(string="銷貨單備註")
    amount_received = fields.Monetary(string="已收金額", currency_field="currency_id")
    amount_receivable = fields.Monetary(
        string="應收帳款",
        currency_field="currency_id",
        compute="_compute_amount_receivable",
        store=True,
    )
    quantity_total = fields.Float(
        string="數量總計",
        compute="_compute_quantity_total",
        store=True,
    )

    @api.depends("amount_total", "amount_received")
    def _compute_amount_receivable(self):
        for order in self:
            order.amount_receivable = order.amount_total - order.amount_received

    @api.depends("order_line.product_uom_qty")
    def _compute_quantity_total(self):
        for order in self:
            order.quantity_total = sum(order.order_line.mapped("product_uom_qty"))

    @api.depends(
        "sales_slip_invoice_number_manual",
        "invoice_ids.name",
        "invoice_ids.state",
        "invoice_ids.move_type",
    )
    def _compute_sales_slip_invoice_number(self):
        for order in self:
            if order.sales_slip_invoice_number_manual:
                order.sales_slip_invoice_number = order.sales_slip_invoice_number_manual
                continue

            invoices = order.invoice_ids.filtered(
                lambda move: move.state != "cancel"
                and move.move_type in ("out_invoice", "out_refund")
                and move.name
                and move.name != "/"
            )
            order.sales_slip_invoice_number = "、".join(invoices.mapped("name"))

    def _inverse_sales_slip_invoice_number(self):
        for order in self:
            order.sales_slip_invoice_number_manual = order.sales_slip_invoice_number

    @api.onchange("partner_id")
    def _onchange_partner_id_fill_sales_slip_fields(self):
        for order in self:
            partner = order.partner_id
            if not partner:
                continue
            order.sales_slip_contact = partner.name if not order.sales_slip_contact else order.sales_slip_contact
            order.sales_slip_phone = partner.phone or partner.mobile
            order.sales_slip_delivery_address = partner.contact_address

    def action_print_sales_slip(self):
        self.ensure_one()
        return self.env.ref("sale_sales_slip.action_report_sale_sales_slip").report_action(self)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sales_slip_spec = fields.Char(string="規格")
    sales_slip_note = fields.Char(string="備註")
