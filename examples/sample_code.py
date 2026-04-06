from typing import Iterable


def filter_positive(data: Iterable) -> list[float | int]:
    """Filter and return only positive numeric values from an iterable.

    Args:
        data: An iterable containing numeric values.

    Returns:
        A list with only the positive numbers from the input.

    Raises:
        TypeError: If data is not iterable or contains non-numeric elements.
    """
    result: list[float | int] = []
    for item in data:
        if not isinstance(item, (int, float)):
            raise TypeError(f"Expected numeric value, got {type(item).__name__}")
        if item > 0:
            result.append(item)
    return result


def multiply_by_two(values: list[float | int]) -> list[float | int]:
    """Multiply each value in the list by two.

    Args:
        values: A list of numeric values.

    Returns:
        A new list with each value multiplied by two.
    """
    return [v * 2 for v in values]


def process_data(data: Iterable) -> list[float | int]:
    """Filter positive numbers from data and double their values.

    Combines filtering of positive values and multiplication by two.

    Args:
        data: An iterable containing numeric values.

    Returns:
        A list where each positive number from the input has been doubled.

    Raises:
        TypeError: If data is not iterable or contains non-numeric elements.

    Examples:
        >>> process_data([1, -2, 3, 0])
        [2, 6]
        >>> process_data([])
        []
    """
    if not hasattr(data, '__iter__'):
        raise TypeError(f"Expected an iterable, got {type(data).__name__}")

    try:
        positive_values = filter_positive(data)
        return multiply_by_two(positive_values)
    except TypeError:
        raise
    except Exception as e:
        raise ValueError(f"Error processing data: {e}") from e
