from langfuse import observe

from .errors import InvalidCoupon

COUPONS = {"WELCOME10": 0.10, "VIP20": 0.20}


@observe(name="apply_discount")
def apply_discount(subtotal: float, coupon: str | None) -> float:
    """Aplica un cupón de descuento al subtotal."""
    if not coupon:
        return subtotal
    normalized_coupon = coupon.upper()
    if normalized_coupon not in COUPONS:
        raise InvalidCoupon(coupon, valid=list(COUPONS))
    rate = COUPONS[normalized_coupon]
    return round(subtotal * (1 - rate), 2)
