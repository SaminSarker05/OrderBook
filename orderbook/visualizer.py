# LLM generated, human reviewed

from decimal import Decimal
from orderbook.order_book import OrderBook
from orderbook.models import Order, Side

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def _color(text, color):
    return f"{color}{text}{Colors.RESET}"

def _bar(quantity, max_quantity, width=18, color=Colors.GREEN):
    if max_quantity <= 0:
        return " " * width
    if quantity <= 0:
        return " " * width

    filled = int((float(quantity) / float(max_quantity)) * width)
    filled = max(1, min(width, filled))
    bar = "█" * filled + "░" * (width - filled)
    return _color(bar, color)

def _fmt_price(value):
    return f"{value:.2f}"

def render_ascii_orderbook(book, depth=10, width=18, clear_screen=False):
    bids, asks = book.get_l2_snapshot(depth=depth)

    if clear_screen:
        print("\033[2J\033[H", end="")

    if not bids and not asks:
        print("Order book is empty")
        return

    max_qty = max(
        [qty for _, qty in bids + asks] or [Decimal("1")],
        default=Decimal("1"),
    )

    max_len = max(len(bids), len(asks))

    best_bid = book.get_best_bid()
    best_ask = book.get_best_ask()

    print(_color("═" * 90, Colors.BOLD))
    print(_color("                      ORDER BOOK", Colors.BOLD))
    print(_color("═" * 90, Colors.BOLD))

    bid_label = _color("BID", Colors.GREEN)
    ask_label = _color("ASK", Colors.RED)
    print(f"{bid_label:^42}{'|':^6}{ask_label:^42}")

    best_bid_text = (
        _color(f"BEST BID: {best_bid if best_bid is not None else '—'}", Colors.GREEN)
        if best_bid is not None
        else _color("BEST BID: —", Colors.GREEN)
    )
    best_ask_text = (
        _color(f"BEST ASK: {best_ask if best_ask is not None else '—'}", Colors.RED)
        if best_ask is not None
        else _color("BEST ASK: —", Colors.RED)
    )

    print()
    print(f"{best_bid_text:^42}{'|':^6}{best_ask_text:^42}")
    print()

    for i in range(max_len):
        bid_price, bid_qty = bids[i] if i < len(bids) else (None, None)
        ask_price, ask_qty = asks[i] if i < len(asks) else (None, None)

        bid_cell = ""
        if bid_price is not None:
            bid_cell = (
                _color(f"{_fmt_price(bid_price):>8}", Colors.GREEN)
                + "  "
                + _color(f"qty:{bid_qty:<6}", Colors.YELLOW)
                + " "
                + _bar(bid_qty, max_qty, width=width, color=Colors.GREEN)
            )

        ask_cell = ""
        if ask_price is not None:
            ask_cell = (
                _bar(ask_qty, max_qty, width=width, color=Colors.RED)
                + " "
                + _color(f"qty:{ask_qty:<6}", Colors.YELLOW)
                + "  "
                + _color(f"{_fmt_price(ask_price):>8}", Colors.RED)
            )

        print(f"{bid_cell:<44}{'|':^6}{ask_cell:>44}")

    print(_color("─" * 90, Colors.BOLD))
    spread = book.get_spread()
    spread_text = _color(f"Spread: {spread if spread is not None else 'n/a'}", Colors.CYAN)
    print(spread_text)
    print(_color("═" * 90, Colors.BOLD))

def demo():
    book = OrderBook()

    # Bids
    book.add_order(Order(1, Side.BUY, Decimal("100.00"), Decimal("5")))
    book.add_order(Order(2, Side.BUY, Decimal("99.50"), Decimal("8")))
    book.add_order(Order(3, Side.BUY, Decimal("99.00"), Decimal("12")))
    book.add_order(Order(4, Side.BUY, Decimal("98.75"), Decimal("7")))
    book.add_order(Order(5, Side.BUY, Decimal("98.25"), Decimal("10")))

    # Asks
    book.add_order(Order(6, Side.SELL, Decimal("101.00"), Decimal("3")))
    book.add_order(Order(7, Side.SELL, Decimal("101.50"), Decimal("6")))
    book.add_order(Order(8, Side.SELL, Decimal("102.00"), Decimal("9")))
    book.add_order(Order(9, Side.SELL, Decimal("102.50"), Decimal("4")))
    book.add_order(Order(10, Side.SELL, Decimal("103.00"), Decimal("11")))

    render_ascii_orderbook(book)

if __name__ == "__main__":
    demo()
