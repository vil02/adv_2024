import functools


def _parse_available(in_line: str) -> frozenset[str]:
    return frozenset(in_line.split(", "))


def _parse_patterns(in_str: str) -> list[str]:
    return in_str.splitlines()


def _parse_input(in_str: str) -> tuple[frozenset[str], list[str]]:
    available, patterns = in_str.split("\n\n")
    return _parse_available(available), _parse_patterns(patterns)


@functools.cache
def is_possible(available: frozenset[str], in_pattern: str) -> bool:
    if not in_pattern:
        return True
    return any(
        is_possible(available, in_pattern.removeprefix(prefix))
        for prefix in available
        if in_pattern.startswith(prefix)
    )


def solve_a(in_str: str) -> int:
    available, patterns = _parse_input(in_str)
    return sum(1 for _ in patterns if is_possible(available, _))


@functools.cache
def count_ways(available: frozenset[str], in_pattern: str) -> int:
    if not in_pattern:
        return 1
    return sum(
        count_ways(available, in_pattern.removeprefix(prefix))
        for prefix in available
        if in_pattern.startswith(prefix)
    )


def solve_b(in_str: str) -> int:
    available, patterns = _parse_input(in_str)
    return sum(count_ways(available, _) for _ in patterns)
