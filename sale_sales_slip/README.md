# Sale Sales Slip

Odoo 18 custom module prototype that extends `sale.order` with sales slip fields and a printable sales slip report.

## Features

- Adds a `document_type` field with `報價單 / 銷售訂單 / 銷貨單`
- Adds a dedicated `銷貨單資訊` page on the sales order form
- Adds a `銷貨單` menu and search filter
- Adds a printable PDF report named `銷貨單`

## Installation

1. Copy the `sale_sales_slip` folder into your Odoo `addons` path.
2. Update Apps List in Odoo.
3. Install `Sale Sales Slip`.

## Notes

- This is a first prototype based on the provided PDF layout.
- You can continue extending numbering rules, confirmation flow, and report styling after validating the field set.
