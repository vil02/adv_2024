import collections


def _parse_input(in_str: str) -> tuple[list[int], list[int]]:
    lefts = []
    rights = []
    for cur_line in in_str.splitlines():
        _l, _r = cur_line.split()
        lefts.append(int(_l))
        rights.append(int(_r))
    return lefts, rights


def solve_a(in_str: str) -> int:
    lefts, rights = _parse_input(in_str)
    lefts = sorted(lefts)
    rights = sorted(rights)
    return sum(abs(_l - _r) for _l, _r in zip(lefts, rights, strict=True))


def solve_b(in_str: str) -> int:
    lefts, rights = _parse_input(in_str)
    counter = collections.Counter(rights)
    return sum(_ * counter[_] for _ in lefts)
