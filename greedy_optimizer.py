
"""
Greedy Algorithms Assignment
Implement three greedy algorithms for delivery optimization.
"""

import json
import time
import heapq


# ============================================================================
# PART 1: PACKAGE PRIORITIZATION (Activity Selection)
# ============================================================================

def maximize_deliveries(time_windows):
    """
    Schedule the maximum number of deliveries given time window constraints.

    Args:
        time_windows (list): List of dicts with
            'delivery_id', 'start', 'end'

    Returns:
        list: Delivery IDs that can be completed.
    """

    # Sort deliveries by their ending time
    sorted_deliveries = sorted(
        time_windows,
        key=lambda delivery: delivery['end']
    )

    selected_deliveries = []
    last_end_time = float('-inf')

    # Choose the earliest finishing delivery that does not overlap
    for delivery in sorted_deliveries:
        if delivery['start'] >= last_end_time:
            selected_deliveries.append(delivery['delivery_id'])
            last_end_time = delivery['end']

    return selected_deliveries


# ============================================================================
# PART 2: TRUCK LOADING (Fractional Knapsack)
# ============================================================================

def optimize_truck_load(packages, weight_limit):
    """
    Maximize total priority value within the truck weight limit.

    Args:
        packages (list): List of dicts with
            'package_id', 'weight', 'priority'
        weight_limit (int): Maximum truck weight

    Returns:
        dict: Total priority, total weight, and packages loaded.
    """

    # Sort packages by priority-to-weight ratio (highest first)
    sorted_packages = sorted(
        packages,
        key=lambda package: package['priority'] / package['weight'],
        reverse=True
    )

    total_priority = 0.0
    total_weight = 0.0
    loaded_packages = []

    for package in sorted_packages:

        # Calculate remaining truck capacity
        remaining_capacity = weight_limit - total_weight

        if remaining_capacity <= 0:
            break

        weight = package['weight']
        priority = package['priority']

        # Take the whole package or the fraction that fits
        fraction = min(1.0, remaining_capacity / weight)

        loaded_packages.append({
            'package_id': package['package_id'],
            'fraction': fraction
        })

        # Update totals
        total_weight += weight * fraction
        total_priority += priority * fraction

    return {
        'total_priority': total_priority,
        'total_weight': total_weight,
        'packages': loaded_packages
    }


# ============================================================================
# PART 3: DRIVER ASSIGNMENT (Interval Scheduling)
# ============================================================================

def minimize_drivers(deliveries):
    """
    Assign deliveries using the minimum number of drivers.

    Args:
        deliveries (list): List of dicts with
            'delivery_id', 'start', 'end'

    Returns:
        dict: Minimum number of drivers and their assignments.
    """

    # Sort deliveries by starting time
    sorted_deliveries = sorted(
        deliveries,
        key=lambda delivery: delivery['start']
    )

    # Min heap stores (available_time, driver_id)
    driver_heap = []

    # Each list represents deliveries assigned to one driver
    assignments = []

    for delivery in sorted_deliveries:

        start = delivery['start']
        end = delivery['end']
        delivery_id = delivery['delivery_id']

        # Reuse the earliest available driver when possible
        if driver_heap and driver_heap[0][0] <= start:
            _, driver_id = heapq.heappop(driver_heap)

        else:
            # Create a new driver if no existing driver is available
            driver_id = len(assignments)
            assignments.append([])

        # Assign the delivery to this driver
        assignments[driver_id].append(delivery_id)

        # Update when the driver becomes available
        heapq.heappush(driver_heap, (end, driver_id))

    return {
        'num_drivers': len(assignments),
        'assignments': assignments
    }


# ============================================================================
# TESTING & BENCHMARKING
# ============================================================================

def load_scenario(filename):
    """Load a scenario from JSON file."""
    with open(f"scenarios/{filename}", "r") as f:
        return json.load(f)


def test_package_prioritization():
    """Test package prioritization with small known cases."""

    print("=" * 70)
    print("TESTING PACKAGE PRIORITIZATION")
    print("=" * 70 + "\n")

    # Test case 1: Non-overlapping deliveries
    test1 = [
        {'delivery_id': 'A', 'start': 1, 'end': 2},
        {'delivery_id': 'B', 'start': 3, 'end': 4},
        {'delivery_id': 'C', 'start': 5, 'end': 6}
    ]

    result1 = maximize_deliveries(test1)

    print("Test 1: Non-overlapping")
    print("  Expected: 3 deliveries")
    print(f"  Got: {len(result1)} deliveries")
    print(f"  {'PASS' if len(result1) == 3 else 'FAIL'}\n")

    # Test case 2: All overlapping
    test2 = [
        {'delivery_id': 'A', 'start': 1, 'end': 5},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 3, 'end': 6}
    ]

    result2 = maximize_deliveries(test2)

    print("Test 2: All overlapping")
    print("  Expected: 1 delivery")
    print(f"  Got: {len(result2)} deliveries")
    print(f"  Result: {result2}")
    print(f"  {'PASS' if len(result2) == 1 else 'FAIL'}\n")

    # Test case 3: Mixed overlapping
    test3 = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 5},
        {'delivery_id': 'C', 'start': 4, 'end': 7},
        {'delivery_id': 'D', 'start': 6, 'end': 9}
    ]

    result3 = maximize_deliveries(test3)

    print("Test 3: Mixed overlapping")
    print("  Expected: 2 deliveries")
    print(f"  Got: {len(result3)} deliveries")
    print(f"  Result: {result3}")
    print(f"  {'PASS' if len(result3) == 2 else 'FAIL'}\n")


def test_truck_loading():
    """Test truck loading with small known cases."""

    print("=" * 70)
    print("TESTING TRUCK LOADING")
    print("=" * 70 + "\n")

    # Test case 1: All packages fit
    packages1 = [
        {'package_id': 'A', 'weight': 10, 'priority': 60},
        {'package_id': 'B', 'weight': 20, 'priority': 100}
    ]

    result1 = optimize_truck_load(packages1, 50)

    print("Test 1: All packages fit")
    print("  Expected: Priority = 160, weight = 30")
    print(
        f"  Got: Priority = {result1['total_priority']}, "
        f"weight = {result1['total_weight']}"
    )
    print(
        f"  {'PASS' if result1['total_priority'] == 160 else 'FAIL'}\n"
    )

    # Test case 2: Fractional required
    packages2 = [
        {'package_id': 'A', 'weight': 10, 'priority': 60},
        {'package_id': 'B', 'weight': 20, 'priority': 100},
        {'package_id': 'C', 'weight': 30, 'priority': 120}
    ]

    result2 = optimize_truck_load(packages2, 50)

    print("Test 2: Fractional knapsack")
    print("  Expected: A full, B full, C partial")
    print("  Expected priority: 240")
    print(f"  Got priority: {result2['total_priority']}")
    print(f"  Got weight: {result2['total_weight']}")
    print(f"  Packages: {result2['packages']}")
    print(
        f"  {'PASS' if abs(result2['total_priority'] - 240) < 0.001 else 'FAIL'}\n"
    )


def test_driver_assignment():
    """Test driver assignment with small known cases."""

    print("=" * 70)
    print("TESTING DRIVER ASSIGNMENT")
    print("=" * 70 + "\n")

    # Test case 1: All non-overlapping
    deliveries1 = [
        {'delivery_id': 'A', 'start': 1, 'end': 2},
        {'delivery_id': 'B', 'start': 3, 'end': 4},
        {'delivery_id': 'C', 'start': 5, 'end': 6}
    ]

    result1 = minimize_drivers(deliveries1)

    print("Test 1: Non-overlapping")
    print("  Expected: 1 driver")
    print(f"  Got: {result1['num_drivers']} drivers")
    print(
        f"  {'PASS' if result1['num_drivers'] == 1 else 'FAIL'}\n"
    )

    # Test case 2: All overlapping
    deliveries2 = [
        {'delivery_id': 'A', 'start': 1, 'end': 5},
        {'delivery_id': 'B', 'start': 2, 'end': 6},
        {'delivery_id': 'C', 'start': 3, 'end': 7}
    ]

    result2 = minimize_drivers(deliveries2)

    print("Test 2: All overlapping")
    print("  Expected: 3 drivers")
    print(f"  Got: {result2['num_drivers']} drivers")
    print(
        f"  {'PASS' if result2['num_drivers'] == 3 else 'FAIL'}\n"
    )

    # Test case 3: Mixed deliveries
    deliveries3 = [
        {'delivery_id': 'A', 'start': 1, 'end': 3},
        {'delivery_id': 'B', 'start': 2, 'end': 4},
        {'delivery_id': 'C', 'start': 4, 'end': 6},
        {'delivery_id': 'D', 'start': 5, 'end': 7}
    ]

    result3 = minimize_drivers(deliveries3)

    print("Test 3: Mixed overlapping")
    print("  Expected: 2 drivers")
    print(f"  Got: {result3['num_drivers']} drivers")
    print(f"  Assignments: {result3['assignments']}")
    print(
        f"  {'PASS' if result3['num_drivers'] == 2 else 'FAIL'}\n"
    )


def benchmark_scenarios():
    """Benchmark all algorithms on realistic scenarios."""

    print("\n" + "=" * 70)
    print("BENCHMARKING ON REALISTIC SCENARIOS")
    print("=" * 70 + "\n")

    # Benchmark package prioritization
    print("Scenario 1: Package Prioritization (50 deliveries)")
    print("-" * 70)

    data = load_scenario("package_prioritization.json")

    start = time.perf_counter()
    result = maximize_deliveries(data)
    elapsed = time.perf_counter() - start

    print(f"  Deliveries scheduled: {len(result)} out of {len(data)}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")

    # Benchmark truck loading
    print("Scenario 2: Truck Loading (100 packages, 500 lb limit)")
    print("-" * 70)

    data = load_scenario("truck_loading.json")

    start = time.perf_counter()
    result = optimize_truck_load(
        data['packages'],
        data['truck_capacity']
    )
    elapsed = time.perf_counter() - start

    print(f"  Total priority loaded: {result['total_priority']:.2f}")
    print(f"  Total weight loaded: {result['total_weight']:.2f} lbs")
    print(f"  Packages used: {len(result['packages'])}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")

    # Benchmark driver assignment
    print("Scenario 3: Driver Assignment (60 deliveries)")
    print("-" * 70)

    data = load_scenario("driver_assignment.json")

    start = time.perf_counter()
    result = minimize_drivers(data)
    elapsed = time.perf_counter() - start

    print(f"  Drivers needed: {result['num_drivers']}")
    print(f"  Runtime: {elapsed * 1000:.4f} ms\n")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == "__main__":

    print("GREEDY ALGORITHMS ASSIGNMENT")
    print("Running tests and performance benchmarks.\n")

    # Run all three algorithm tests
    test_package_prioritization()
    test_truck_loading()
    test_driver_assignment()

    # Run benchmarks on generated delivery scenarios
    benchmark_scenarios()

    print("\nALL TESTS AND BENCHMARKS COMPLETED")
