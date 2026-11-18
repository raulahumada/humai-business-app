import random
import time

from langfuse import get_client, observe

from .catalog import PRODUCTS
from .errors import OutOfStock, report_error
from .pricing import apply_discount


@observe(name="reserve_stock")
def reserve_stock(cart: dict[str, int]) -> float:
    subtotal = 0.0
    for sku, qty in cart.items():
        product = PRODUCTS[sku]
        if product["stock"] < qty:
            raise OutOfStock(sku, requested=qty, available=product["stock"])
        subtotal += product["price"] * qty
    return subtotal


@observe(name="charge_payment", as_type="generation")
def charge_payment(amount: float) -> str:
    time.sleep(random.uniform(0.05, 0.3))  # simula pasarela de pago
    get_client().update_current_generation(
        model="payment-gateway",
        usage_details={"input": 1, "output": 1},
    )
    return f"pay_{random.randint(1000, 9999)}"


@observe(name="checkout")
def checkout(cart: dict[str, int], coupon: str | None = None) -> dict:
    try:
        subtotal = reserve_stock(cart)
        total = apply_discount(subtotal, coupon)
        return {"payment_id": charge_payment(total), "total": total}
    except Exception as exc:
        report_error(exc)
        raise
