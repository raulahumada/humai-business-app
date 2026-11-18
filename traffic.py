"""Genera tráfico sintético de compras hacia Langfuse."""

import random
import sys

from dotenv import load_dotenv

load_dotenv()

from langfuse import get_client  # noqa: E402

from shop.catalog import PRODUCTS  # noqa: E402
from shop.checkout import checkout  # noqa: E402


def main(n: int = 40) -> None:
    skus = list(PRODUCTS)
    for _ in range(n):
        cart = {s: random.randint(1, 2) for s in random.sample(skus, random.randint(1, 3))}
        coupon = random.choice([None, "WELCOME10", "VIP20", "welcome10", "vip20"])
        try:
            checkout(cart, coupon)
        except Exception:
            pass
    get_client().flush()
    print(f"{n} checkouts enviados")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
