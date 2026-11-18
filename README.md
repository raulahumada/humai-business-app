# humai-business-app

E-commerce demo (carrito, cupones, stock, checkout) **instrumentado con Langfuse**.
Es el **producto observado** por el agente de [`langfuse-ops`](../presentation/langfuse-ops): genera trazas y errores reales para que el agente los diagnostique y proponga un PR.

## Estructura

```
shop/
├── catalog.py    # productos y stock (sku-hoodie tiene stock 0 a propósito)
├── pricing.py    # apply_discount: cupones WELCOME10 y VIP20
├── checkout.py   # checkout → reserve_stock → apply_discount → charge_payment
└── errors.py     # ShopError, OutOfStock, InvalidCoupon, report_error()
traffic.py        # genera N checkouts sintéticos
tests/            # pytest
```

Cada paso lleva `@observe` de Langfuse; `charge_payment` se registra como *generation* (simula una pasarela de pago).

## Errores (a propósito)

| Código | Cuándo | Tipo |
|---|---|---|
| `INVALID_COUPON` | El cupón viene en minúscula (`welcome10`, `vip20`): `COUPONS` distingue mayúsculas | **Bug de código**: el agente debería proponer un PR (p. ej. normalizar con `.upper()` y agregar un test) |
| `OUT_OF_STOCK` | Se pide más de lo que hay (el buzo tiene stock 0) | Error de negocio esperado |

`report_error()` marca el span con `level=ERROR` y publica metadata `error.code`, `error.type`, `error.location`, `error.stacktrace` y `error.context`. El MCP de `langfuse-ops` lee ese contrato para armar el diagnóstico.

## Uso

```bash
uv sync
cp .env.example .env     # LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY
uv run python traffic.py 40     # envía 40 checkouts a Langfuse
uv run pytest
```

Las trazas **no se generan solas**: solo existen cuando se ejecuta `traffic.py` (o cuando una app real usa este código). Para la demo local, las keys son las del Langfuse de `langfuse-ops/infra` (`pk-lf-local-demo` / `sk-lf-local-demo`).
