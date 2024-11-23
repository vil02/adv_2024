def _parse_input(in_str: str) -> list[int]:
    def _proc_single_line(in_line: str) -> int:
        return len(in_line)

    return [_proc_single_line(_) for _ in in_str.splitlines()]


def solve_a(in_str: str) -> int:
    data = _parse_input(in_str)
    return sum(data)


def solve_b(in_str: str) -> int:
    data = _parse_input(in_str)
    return 2 * sum(data)
