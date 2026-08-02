import time
import random
import statistics
from decimal import Decimal

from orderbook.models import Order, Side, OrderType
from orderbook.matching_engine import MatchingEngine

def percentile(values, p):
    if not values:
        return 0.0

    sorted_vals = sorted(values)
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])

    index = (len(sorted_vals) - 1) * p
    lower = int(index)
    upper = min(lower + 1, len(sorted_vals) - 1)
    weight = index - lower

    return float(sorted_vals[lower] + (sorted_vals[upper] - sorted_vals[lower]) * weight)

def fmt_ns(value_ns):
    # convert ns to a more helpful unit 
    if value_ns >= 1_000_000:
        return f"{value_ns / 1_000_000:.3f} ms"
    if value_ns >= 1_000:
        return f"{value_ns / 1_000:.3f} µs"
    return f"{value_ns:.0f} ns"

def run_benchmark(num_orders: int = 50_000):
    engine = MatchingEngine()
    random.seed(42)
    # hold latency to process each order
    latencies_ns = []
    
    prices = [Decimal(str(p)) for p in range(95, 106)]
    sides = [Side.BUY, Side.SELL]
    
    start_time = time.perf_counter()
    
    for i in range(1, num_orders + 1):
        side = random.choice(sides)
        price = random.choice(prices)
        quantity = Decimal(str(random.randint(1, 100)))
        
        order = Order(
            order_id=i,
            side=side,
            price=price,
            quantity=quantity,
            order_type=OrderType.LIMIT
        )
        
        t0 = time.perf_counter_ns()
        engine.process_order(order)
        t1 = time.perf_counter_ns()
        
        latencies_ns.append(t1 - t0)
    
    end_time = time.perf_counter()
    total_duration_sec = end_time - start_time
    throughput = num_orders / total_duration_sec if total_duration_sec > 0 else float("inf")
    
    # print(f"Total Elapsed Time  : {total_duration_sec:.4f} seconds")
    print("\n=== OrderBook Matching Benchmark ===")
    print(f"Orders processed : {num_orders:,}")
    print(f"Total time       : {total_duration_sec:.4f} seconds")
    print(f"Throughput       : {throughput:,.2f} orders/second")
    print()

    print(f"{'Metric':<10}{'Value':>18}")
    print("-" * 30)
    print(f"{'Min':<10}{fmt_ns(min(latencies_ns)):>18}")
    print(f"{'Max':<10}{fmt_ns(max(latencies_ns)):>18}")
    print(f"{'Mean':<10}{fmt_ns(int(statistics.mean(latencies_ns))):>18}")
    print(f"{'Median':<10}{fmt_ns(int(statistics.median(latencies_ns))):>18}")
    print(f"{'P50':<10}{fmt_ns(int(percentile(latencies_ns, 0.50))):>18}")
    print(f"{'P95':<10}{fmt_ns(int(percentile(latencies_ns, 0.95))):>18}")
    print(f"{'P99':<10}{fmt_ns(int(percentile(latencies_ns, 0.99))):>18}")

if __name__ == "__main__":
    run_benchmark(50_000)
