import csv
import timeit
from typing import List
from custom_csv import CustomCsvReader, CustomCsvWriter


def generate_synthetic_data(rows: int = 10_000, cols: int = 5) -> List[List[str]]:
    """Generate reproducible CSV-like test data."""
    data = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if j == 0:
                row.append(f"row{i}_col{j}")
            elif j == 1:
                row.append(f"value, with comma {i}-{j}")
            elif j == 2:
                row.append(f"line1-{i}-{j}\nline2-{i}-{j}")
            elif j == 3:
                row.append(f"plain{i}-{j}")
            else:
                row.append(f'with "quote" {i}-{j}')
        data.append(row)
    return data


def benchmark_custom_write():
    """Benchmark custom CSV writer."""
    data = generate_synthetic_data()
    with open("/tmp/custom_out.csv", "w", newline="") as f:
        writer = CustomCsvWriter(f)
        writer.writerows(data)


def benchmark_std_write():
    """Benchmark standard CSV writer."""
    data = generate_synthetic_data()
    with open("/tmp/std_out.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def benchmark_custom_read():
    """Benchmark custom CSV reader."""
    with open("/tmp/custom_out.csv", "r", newline="") as f:
        reader = CustomCsvReader(f)
        for _ in reader:
            pass


def benchmark_std_read():
    """Benchmark standard CSV reader."""
    with open("/tmp/std_out.csv", "r", newline="") as f:
        reader = csv.reader(f)
        for _ in reader:
            pass


def run_benchmarks(repeat: int = 5):
    """Run read/write benchmarks and print results."""
    print("Generating synthetic data...")
    data = generate_synthetic_data()
    
    print(f"Benchmarking with {len(data)} rows and {len(data[0]) if data else 0} columns...")
    print()
    
    custom_write = timeit.timeit(
        "benchmark_custom_write()", globals=globals(), number=repeat
    )
    std_write = timeit.timeit(
        "benchmark_std_write()", globals=globals(), number=repeat
    )
    custom_read = timeit.timeit(
        "benchmark_custom_read()", globals=globals(), number=repeat
    )
    std_read = timeit.timeit("benchmark_std_read()", globals=globals(), number=repeat)

    print("=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Custom writer avg time: {custom_write / repeat:.6f} seconds")
    print(f"Standard writer avg time: {std_write / repeat:.6f} seconds")
    print(f"Custom writer slowdown: {(custom_write / repeat) / (std_write / repeat):.2f}x")
    print()
    print(f"Custom reader avg time: {custom_read / repeat:.6f} seconds")
    print(f"Standard reader avg time: {std_read / repeat:.6f} seconds")
    print(f"Custom reader slowdown: {(custom_read / repeat) / (std_read / repeat):.2f}x")
    print("=" * 60)


if __name__ == "__main__":
    run_benchmarks()
