import itertools


def _get_sizes(in_str: str) -> tuple[int, int]:
    lines = in_str.splitlines()
    x_size = len(lines[0])
    y_size = len(lines)
    return x_size, y_size


def _get_height(in_str: str, in_col_num: int) -> int:
    _, y_size = _get_sizes(in_str)
    lines = in_str.splitlines()
    return sum(1 for _ in range(y_size) if lines[_][in_col_num] == "#") - 1


def _heights(in_str: str) -> list[int]:
    x_size, _ = _get_sizes(in_str)
    return [_get_height(in_str, _) for _ in range(x_size)]


def _is_key(in_str: str) -> bool:
    lines = in_str.splitlines()
    return set(lines[0]) == {"#"}


def _parse(in_str: str) -> tuple[bool, list[int]]:
    return _is_key(in_str), _heights(in_str)


def _parse_input(in_str: str) -> tuple[list[list[int]], list[list[int]]]:
    keys = []
    locks = []
    for _ in in_str.split("\n\n"):
        is_key, heights = _parse(_)
        if is_key:
            keys.append(heights)
        else:
            locks.append(heights)
    return locks, keys


def does_fit(lock: list[int], key: list[int]) -> bool:
    return all(_l + _k <= len(lock) for _l, _k in zip(lock, key, strict=True))


def solve_a(in_str: str) -> int:
    locks, keys = _parse_input(in_str)
    return sum(1 for _l, _k in itertools.product(locks, keys) if does_fit(_l, _k))
