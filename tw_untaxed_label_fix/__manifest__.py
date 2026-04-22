{
    "name": "TW Untaxed Label Fix",
    "summary": "Change Untaxed Amount wording to 未稅金額 on invoice and quotation reports.",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations",
    "author": "OpenAI Codex",
    "license": "LGPL-3",
    "depends": ["account", "sale_management"],
    "data": [
        "views/report_tax_totals_fix.xml",
        "views/report_invoice_cleanup.xml",
        "views/account_move_views.xml",
        "report/tw_invoice_report.xml",
    ],
    "installable": True,
    "application": False,
}
