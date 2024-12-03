import re

_PATTERN = r"mul\(\d{1,3},\d{1,3}\)"


def _evaluate(in_str: str) -> int:
    assert in_str.startswith("mul(")
    assert in_str.endswith(")")
    str_a, str_b = in_str[4:-1].split(",")
    return int(str_a) * int(str_b)


def solve_a(in_str: str) -> int:
    return sum(_evaluate(_) for _ in re.findall(_PATTERN, in_str))


def _is_enabled(in_str: str, cur_pos: int) -> bool:
    assert 0 <= cur_pos < len(in_str)
    last_do_pos = in_str.rfind("do()", 0, cur_pos)

    return "don't()" not in in_str[max(last_do_pos, 0) : cur_pos]


def solve_b(in_str: str) -> int:
    return sum(
        _evaluate(m.group())
        for m in re.finditer(_PATTERN, in_str)
        if _is_enabled(in_str, m.start())
    )
