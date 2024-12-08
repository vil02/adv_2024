import collections
import itertools
import typing

Pair = tuple[int, int]
PosSet = set[Pair]


def _parse_input(in_str: str) -> tuple[dict[str, PosSet], Pair]:
    res = collections.defaultdict(set)
    lines = in_str.splitlines()
    size_y = len(lines)
    size_x = len(lines[0])
    for pos_y, line in enumerate(lines):
        assert size_x == len(line)
        for pos_x, char in enumerate(line):
            if char != ".":
                res[char].add((pos_x, pos_y))
    return res, (size_x, size_y)


def _diff(start: Pair, end: Pair) -> Pair:
    return end[0] - start[0], end[1] - start[1]


def _shift(pos: Pair, shift: Pair) -> Pair:
    return pos[0] + shift[0], pos[1] + shift[1]


def _get_antinodes_a(pos_a: Pair, pos_b: Pair, limits) -> PosSet:
    res = set()
    new_pos = _shift(pos_b, _diff(pos_a, pos_b))
    if _is_in(new_pos, limits):
        res.add(new_pos)
    new_pos = _shift(pos_a, _diff(pos_b, pos_a))
    if _is_in(new_pos, limits):
        res.add(new_pos)
    return res


def _is_in(pos: Pair, size: Pair) -> bool:
    return all(0 <= _p < _s for _p, _s in zip(pos, size, strict=True))


def _iterate(start_pos: Pair, iter_dir: Pair, limits: Pair) -> PosSet:
    res = set()
    new_pos = start_pos
    while _is_in(new_pos, limits):
        res.add(new_pos)
        new_pos = _shift(new_pos, iter_dir)
    return res


def _get_antinodes_b(pos_a: Pair, pos_b: Pair, limits: Pair) -> PosSet:
    return _iterate(pos_b, _diff(pos_a, pos_b), limits) | _iterate(
        pos_a, _diff(pos_b, pos_a), limits
    )


def _get_all_antinodes(
    get_antinodes: typing.Callable[[Pair, Pair, Pair], PosSet]
) -> typing.Callable[[PosSet, Pair], PosSet]:
    def _all_antinodes(positions: PosSet, limits: Pair) -> PosSet:
        return {
            antinode
            for pos_a, pos_b in itertools.combinations(positions, 2)
            for antinode in get_antinodes(pos_a, pos_b, limits)
        }

    return _all_antinodes


def _get_solve(
    all_antinodes: typing.Callable[[PosSet, Pair], PosSet]
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        data, limits = _parse_input(in_str)
        res = {antinode for _ in data.values() for antinode in all_antinodes(_, limits)}
        return len(res)

    return _solve


solve_a = _get_solve(_get_all_antinodes(_get_antinodes_a))
solve_b = _get_solve(_get_all_antinodes(_get_antinodes_b))
