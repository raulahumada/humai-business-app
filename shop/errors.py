"""Errores de dominio con contexto + reporte a Langfuse para diagnosticar."""

import json
import traceback

from langfuse import get_client


class ShopError(Exception):
    """Error de negocio con código estable y contexto estructurado."""

    code = "SHOP_ERROR"

    def __init__(self, message: str, **context):
        super().__init__(message)
        self.context = context


class OutOfStock(ShopError):
    code = "OUT_OF_STOCK"

    def __init__(self, sku: str, requested: int, available: int):
        super().__init__(
            f"Sin stock de '{sku}': se pidieron {requested} y hay {available} disponibles",
            sku=sku, requested=requested, available=available,
        )


class InvalidCoupon(ShopError):
    code = "INVALID_COUPON"

    def __init__(self, coupon: str, valid: list[str]):
        super().__init__(
            f"Cupón '{coupon}' no válido. Cupones válidos: {', '.join(valid)} "
            "(la búsqueda distingue mayúsculas y minúsculas)",
            coupon=coupon, valid=valid,
        )


def report_error(exc: Exception) -> None:
    tb = traceback.extract_tb(exc.__traceback__)
    last = tb[-1] if tb else None
    meta = {
        "error.type": type(exc).__name__,
        "error.code": getattr(exc, "code", "UNEXPECTED"),
        "error.location": f"{last.filename.split('/')[-1]}:{last.lineno} en {last.name}" if last else None,
        "error.stacktrace": "".join(traceback.format_exception(exc))[-1500:],
    }
    ctx = getattr(exc, "context", None)
    if ctx:
        meta["error.context"] = json.dumps(ctx, ensure_ascii=False)
    get_client().update_current_span(
        level="ERROR", status_message=f"[{meta['error.code']}] {exc}", metadata=meta
    )
