from langfuse import observe

COUPONS = {"WELCOME10": 0.10, "VIP20": 0.20}


@observe(name="apply_discount")
def apply_discount(subtotal: float, coupon: str | None) -> float:
    """Aplica un cupón de descuento al subtotal."""
    if not coupon:
        return subtotal
    rate = COUPONS[coupon]
    return round(subtotal * (1 - rate), 2)
