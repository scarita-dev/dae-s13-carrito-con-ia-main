"""Your cart. Complete every TODO until `python manage.py test` is green.

The rules (money, stock, coupons, checkout) are in README.md and in shop/domain.py. Do not change
shop/domain.py or the tests. Money is Decimal (never float) and the price always comes from the
catalog, never from the request.
"""
from decimal import Decimal  # noqa: F401

from shop.domain import (  # noqa: F401  (you will need most of these)
    COUPONS,
    IGV_RATE,
    CartError,
    InvalidCoupon,
    InvalidQuantity,
    Line,
    OutOfStock,
    UnknownProduct,
    fmt,
    money,
)


class Cart:
    def __init__(self, catalog):
        self._catalog = catalog  # sku -> Product (price Decimal, stock int)
        self._qty = {}  # sku -> quantity, in insertion order
        self._coupon = None  # one coupon per cart

    # --- persistence between requests (already done) ---
    def to_state(self):
        return {"qty": dict(self._qty), "coupon": self._coupon}

    @classmethod
    def from_state(cls, catalog, state):
        cart = cls(catalog)
        cart._qty = {sku: int(q) for sku, q in state.get("qty", {}).items() if sku in catalog}
        cart._coupon = state.get("coupon")
        return cart

    # --- lines ---
    def add(self, sku, qty=1):
        """Add qty units of a catalog product to the cart."""
        if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
            raise InvalidQuantity(f"Invalid quantity: {qty!r}")
        product = self._catalog.get(sku)
        if product is None:
            raise UnknownProduct(f"Unknown product {sku!r}")
        in_cart = self._qty.get(sku, 0)
        if in_cart + qty > product.stock:
            raise OutOfStock(f"{sku}: requested {qty}, already in cart {in_cart}, stock {product.stock}")
        self._qty[sku] = in_cart + qty

    def remove(self, sku, qty=None):
        """Remove a whole line or some units, never leaving a negative quantity."""
        if sku not in self._qty:
            raise UnknownProduct(f"{sku!r} is not in the cart")
        if qty is None:
            del self._qty[sku]
            return
        if isinstance(qty, bool) or not isinstance(qty, int) or qty < 1:
            raise InvalidQuantity(f"Invalid quantity: {qty!r}")
        remaining = self._qty[sku] - qty
        if remaining <= 0:
            del self._qty[sku]
        else:
            self._qty[sku] = remaining

    def qty_of(self, sku):
        return self._qty.get(sku, 0)

    def lines(self):
        """Return one line per sku in insertion order, priced from the catalog."""
        return [
            Line(sku, self._catalog[sku].name, self._catalog[sku].price, qty)
            for sku, qty in self._qty.items()
        ]

    # --- coupon and totals ---
    def apply_coupon(self, code):
        """Validate and store exactly one coupon: applying again replaces the previous one."""
        normalized = code.strip().upper() if isinstance(code, str) else ""
        if normalized not in COUPONS:
            raise InvalidCoupon(f"Unknown coupon: {normalized!r}")
        self._coupon = normalized

    def subtotal(self):
        """Sum of catalog price times quantity, rounded to cents with Decimal."""
        return money(sum((line.total for line in self.lines()), Decimal("0")))

    def discount(self):
        """TODO: percent coupon = subtotal * pct / 100 rounded half up; fixed coupon = the amount, but
        never more than the subtotal; no coupon = Decimal('0.00')."""
        raise NotImplementedError("TODO: discount")

    def igv(self):
        """TODO: 18 % of (subtotal - discount), rounded half up."""
        raise NotImplementedError("TODO: igv")

    def total(self):
        """TODO: (subtotal - discount) + igv."""
        raise NotImplementedError("TODO: total")

    def summary(self):
        """TODO: the dict the API returns. Keys: lines (list of dicts with sku, name, unit_price,
        qty, line_total as 2-decimal strings), coupon, subtotal, discount, igv, total (strings via fmt)."""
        raise NotImplementedError("TODO: summary")

    # --- checkout ---
    def checkout(self):
        """TODO: empty cart -> CartError; stock is checked AGAIN (OutOfStock); on success the catalog stock
        goes down by what was bought, the cart is emptied and the summary of the order is returned."""
        raise NotImplementedError("TODO: checkout")


def add_from_payload(cart, payload):
    """TODO: translate the JSON body of POST /api/cart/items/ ({"sku": ..., "qty": ...}) into a cart.add
    call. The body is untrusted: if it is not a dict with a string «sku», raise CartError. The price is
    NOT part of the contract: the catalog is the only source of prices."""
    raise NotImplementedError("TODO: add_from_payload")
