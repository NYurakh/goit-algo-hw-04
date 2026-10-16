import random
import statistics
import timeit


def insertion_sort(arr):
    result = arr.copy()

    for i in range(1, len(result)):
        key = result[i]
        j = i - 1

        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = key

    return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2

    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def generate_data(size):
    random_data = [random.randint(0, 100000) for _ in range(size)]
    sorted_data = sorted(random_data)
    reversed_data = sorted_data[::-1]

    nearly_sorted = sorted_data.copy()
    for _ in range(max(1, size // 100)):
        i, j = random.sample(range(size), 2)
        nearly_sorted[i], nearly_sorted[j] = (nearly_sorted[j], nearly_sorted[i])

    return {
        "Random": random_data,
        "Sorted": sorted_data,
        "Reversed": reversed_data,
        "Nearly sorted": nearly_sorted,
    }


def benchmark(sort_function, data, repeats=5):
    measurements = timeit.repeat(lambda: sort_function(data), repeat=repeats, number=1)

    return statistics.median(measurements) * 1000


def main():
    random.seed(42)

    algorithms = {
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Timsort": sorted,
    }

    sizes = [100, 1000, 5000]

    for size in sizes:
        print(f"\nArray size: {size}")
        print("-" * 65)

        datasets = generate_data(size)

        for data_type, data in datasets.items():
            print(f"\nDataset: {data_type}")

            expected = sorted(data)

            for name, function in algorithms.items():
                assert function(data) == expected, f"{name} returned incorrect results"

                execution_time = benchmark(function, data)

                print(f"{name:<20}: {execution_time:.4f} ms")


if __name__ == "__main__":
    main()
