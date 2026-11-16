# Discount codes

`apply_discount(total_cents, code, today)` returns the order total, in cents, after
the code is applied. It must follow these five rules.

1. An empty code (`""`) leaves the total unchanged.
2. Codes are not case-sensitive: `"save10"` and `"Save10"` work exactly like `"SAVE10"`.
3. An unknown code raises `ValueError`.
4. A code can be used up to and including its last day. From the next day on, it
   raises `ValueError`.
5. The discount is a whole number of cents, rounded down. For example, 10 percent off
   1999 cents is 199 cents off, so the total is 1800.
