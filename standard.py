import sys
from array import array


class IntScanner:
    """Fast integer scanner over a bytes buffer.

    Purpose:
        Parse integers from a bytes buffer using next_int().

    Args:
        data: Entire input as bytes.
    """

    def __init__(self, data: bytes) -> None:
        """Initialize the scanner.

        Args:
            data: Entire input as bytes.
        """
        self._data = data
        self._length = len(data)
        self._position = 0

    def next_int(self) -> int:
        """Return the next integer from the buffer.

        Returns:
            The next parsed integer.
        """
        data = self._data
        length = self._length
        position = self._position

        while position < length and data[position] <= 32:
            position += 1

        value = 0
        while position < length and data[position] > 32:
            value = value * 10 + (data[position] - 48)
            position += 1

        self._position = position
        return value


class FenwickTree:
    """Fenwick Tree (Binary Indexed Tree) for prefix sums.

    Purpose:
        Support point updates and prefix sum queries in O(log n).

    Args:
        size: Maximum index supported (1-indexed).
    """

    def __init__(self, size: int) -> None:
        """Create a Fenwick Tree initialized with zeros.

        Args:
            size: Maximum index supported (1-indexed).
        """
        self._size = size
        self._tree = array("I", [0]) * (size + 1)

    def add(self, index: int, delta: int) -> None:
        """Add delta to position index.

        Args:
            index: 1-indexed position to update.
            delta: Value to add.
        """
        size = self._size
        tree = self._tree
        while index <= size:
            tree[index] += delta
            index += index & -index

    def prefix_sum(self, index: int) -> int:
        """Compute sum of positions in range [1..index].

        Args:
            index: 1-indexed end position.

        Returns:
            The prefix sum up to index.
        """
        result = 0
        tree = self._tree
        while index > 0:
            result += tree[index]
            index -= index & -index
        return result


def build_final_scroll(
    operation_types: array,
    operation_from_values: array,
    operation_to_values: array,
    max_value: int,
) -> list[int]:
    """Reconstruct the final scroll by processing operations backwards.

    Args:
        operation_types: Operation types (1, 2, 3) in input order.
        operation_from_values: The x parameter for each operation.
        operation_to_values: The y parameter for each operation (0 for type 1).
        max_value: Maximum value appearing in the input.

    Returns:
        The final scroll as a list of integers.
    """
    value_mapping = array("I", range(max_value + 1))
    reversed_scroll: list[int] = []

    operation_count = len(operation_types)
    for operation_index in range(operation_count - 1, -1, -1):
        operation_type = operation_types[operation_index]
        from_value = operation_from_values[operation_index]

        if operation_type == 1:
            reversed_scroll.append(value_mapping[from_value])
            continue

        to_value = operation_to_values[operation_index]
        if operation_type == 2:
            value_mapping[from_value] = value_mapping[to_value]
        else:
            value_mapping[from_value], value_mapping[to_value] = (
                value_mapping[to_value],
                value_mapping[from_value],
            )

    reversed_scroll.reverse()
    return reversed_scroll


def count_inversions(values: list[int], max_value: int) -> int:
    """Count inversions in values using a Fenwick Tree.

    Args:
        values: Array for which to compute inversion count.
        max_value: Maximum value in values (sizes the Fenwick Tree).

    Returns:
        The inversion count.
    """
    fenwick_tree = FenwickTree(max_value)
    inversion_count = 0
    seen_count = 0

    for current_value in values:
        less_or_equal_count = fenwick_tree.prefix_sum(current_value)
        inversion_count += seen_count - less_or_equal_count
        fenwick_tree.add(current_value, 1)
        seen_count += 1

    return inversion_count


def main() -> None:
    """Read input, compute the final scroll and inversion count, and print."""
    input_data = sys.stdin.buffer.read()
    scanner = IntScanner(input_data)

    operation_count = scanner.next_int()

    operation_types = array("B")
    operation_from_values = array("I")
    operation_to_values = array("I")

    max_value_seen = 1
    for _ in range(operation_count):
        operation_type = scanner.next_int()
        from_value = scanner.next_int()
        to_value = 0

        if operation_type != 1:
            to_value = scanner.next_int()
            if to_value > max_value_seen:
                max_value_seen = to_value

        if from_value > max_value_seen:
            max_value_seen = from_value

        operation_types.append(operation_type)
        operation_from_values.append(from_value)
        operation_to_values.append(to_value)

    final_scroll = build_final_scroll(
        operation_types=operation_types,
        operation_from_values=operation_from_values,
        operation_to_values=operation_to_values,
        max_value=max_value_seen,
    )

    inversion_count = count_inversions(final_scroll, max_value_seen)

    sys.stdout.write(" ".join(map(str, final_scroll)) + "\n")
    sys.stdout.write(str(inversion_count) + "\n")


if __name__ == "__main__":
    main()