# OrderBook

Python implementation of order book with price-time priority matching, resting orders, and a terminal-based ASCII visualizer.

## Core Components
- Order and trade models with bid/ask sides and order types
- A doubly linked list to maintain FIFO queue behavior
- Price levels for grouped resting orders
- An order book with best bid/ask and L2 snapshot support
- A matching engine for LIMIT and MARKET orders
- A benchmark script and an ASCII visualizer for exploring market depth

## Project structure
- [orderbook/models.py](orderbook/models.py) — core data models
- [orderbook/doubly_linked_list.py](orderbook/doubly_linked_list.py) — FIFO linked-list structure
- [orderbook/price_level.py](orderbook/price_level.py) — price-level aggregation
- [orderbook/order_book.py](orderbook/order_book.py) — order book logic
- [orderbook/matching_engine.py](orderbook/matching_engine.py) — trade execution logic
- [orderbook/visualizer.py](orderbook/visualizer.py) — terminal ASCII view
- [tests](tests) — unit tests for the core components

## Run locally
```bash
# run tests
python3 -m pytest

# view the ASCII order book
python3 -m orderbook.visualizer

# run the benchmark
python3 benchmark.py
```

## Example visualization
The visualizer prints a simple terminal order book with bids on the left and asks on the right:

```text
╔════════════════════════════════════════════════════════════════════╗
║                            ORDER BOOK                              ║
╠════════════════════════════════════════════════════════════════════╣
║  BID                           |                      ASK          ║
║  BEST BID: 99.50               |               BEST ASK: 101.00    ║
║  99.50 qty:8 ████████░░░░░░░░  | ██████░░░░░░░░░░░ qty:3 101.00    ║
║  99.00 qty:12 ████████████░░░  | ████████░░░░░░░░░ qty:6 101.50    ║
║  ...                                                          ...  ║
╚════════════════════════════════════════════════════════════════════╝
```
