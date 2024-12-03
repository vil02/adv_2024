import re


def _evaluate(in_str: str) -> int:
    _prefix = "mul("
    _suffix = ")"
    assert in_str.startswith(_prefix)
    assert in_str.endswith(_suffix)
    str_a, str_b = in_str.removeprefix(_prefix).removesuffix(_suffix).split(",")
    return int(str_a) * int(str_b)


_PATTERN = r"mul\(\d{1,3},\d{1,3}\)"


def solve_a(in_str: str) -> int:
    return sum(_evaluate(_.group()) for _ in re.finditer(_PATTERN, in_str))


def solve_b(in_str: str) -> int:
    res = 0
    is_enabled = True
    for _ in re.finditer(_PATTERN + r"|do\(\)|don\'t\(\)", in_str):
        if _.group() == "do()":
            is_enabled = True
        elif _.group() == "don't()":
            is_enabled = False
        elif is_enabled:
            res += _evaluate(_.group())
    return res
