"""Discount codes for the shop's checkout."""

from datetime import date

# code: (percent off, last day the code can be used)
CODES = {
    "SAVE10": (10, date(2026, 12, 31)),
    "WELCOME5": (5, date(2026, 11, 30)),
}


def apply_discount(total_cents: int, code: str, today: date) -> int:
    """Return the order total, in cents, after the discount code is applied."""
    if code == "":
        return total_cents
    if code not in CODES:
        raise ValueError(f"unknown code: {code}")
    percent, last_day = CODES[code]
    discount = total_cents * percent // 100
    return total_cents - discount
