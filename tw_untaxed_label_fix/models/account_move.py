from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    tw_report_note = fields.Char(string="報表備註")

    _TW_UPPER_DIGITS = "零壹貳參肆伍陸柒捌玖"
    _TW_SMALL_UNITS = ["", "拾", "佰", "仟"]
    _TW_GROUP_UNITS = ["", "萬", "億", "兆"]

    def _tw_number_to_upper(self, amount):
        number = int(round(amount or 0))
        if number == 0:
            return "零元整"

        groups = []
        while number:
            groups.append(number % 10000)
            number //= 10000

        result = []
        zero_pending = False
        for group_index in range(len(groups) - 1, -1, -1):
            group = groups[group_index]
            if group == 0:
                zero_pending = bool(result)
                continue

            if zero_pending:
                result.append("零")
                zero_pending = False

            group_text = []
            digits = [int(x) for x in f"{group:04d}"]
            for index, digit in enumerate(digits):
                unit_index = 3 - index
                if digit == 0:
                    if group_text and group_text[-1] != "零" and any(d > 0 for d in digits[index + 1:]):
                        group_text.append("零")
                    continue
                group_text.append(self._TW_UPPER_DIGITS[digit])
                group_text.append(self._TW_SMALL_UNITS[unit_index])

            group_string = "".join(group_text).rstrip("零")
            group_string = group_string.replace("壹拾", "拾")
            result.append(group_string + self._TW_GROUP_UNITS[group_index])

        return "".join(result).rstrip("零") + "元整"

    def _get_tw_invoice_format_code(self):
        self.ensure_one()
        return "25"

    def _get_tw_tax_type(self):
        self.ensure_one()
        if self.amount_tax:
            return "taxed"
        if any(line.tax_ids for line in self.invoice_line_ids):
            return "zero"
        return "exempt"

    def _get_tw_invoice_amount_in_words(self):
        self.ensure_one()
        return self._tw_number_to_upper(self.amount_total)
