from shop.pricing import apply_discount


def test_no_coupon():
    assert apply_discount(100, None) == 100


def test_uppercase_coupon():
    assert apply_discount(100, "WELCOME10") == 90.0
