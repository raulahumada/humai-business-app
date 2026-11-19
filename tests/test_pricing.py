from shop.pricing import apply_discount


def test_no_coupon():
    assert apply_discount(100, None) == 100


def test_uppercase_coupon():
    assert apply_discount(100, "WELCOME10") == 90.0


def test_lowercase_coupon_is_accepted():
    assert apply_discount(100, "welcome10") == 90.0


def test_mixed_case_coupon_is_accepted():
    assert apply_discount(100, "ViP20") == 80.0
