import typing

Pos = tuple[int, int]
HeightMap = dict[Pos, int]


def _parse_input(in_str: str) -> tuple[HeightMap, list[Pos]]:
    starts = []
    res = {}
    lines = in_str.splitlines()
    for y_pos, line in enumerate(lines):
        for x_pos, char in enumerate(line):
            cur_pos = (x_pos, y_pos)
            if char == "0":
                starts.append(cur_pos)
            res[cur_pos] = int(char)
    return res, starts


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_DIRS = (_N, _S, _W, _E)
assert len(set(_DIRS)) == 4


def _shift(pos: Pos, shift: Pos) -> Pos:
    return pos[0] + shift[0], pos[1] + shift[1]


def _gen_positions(
    cur_pos: Pos, height_map: HeightMap
) -> typing.Generator[Pos, None, None]:
    new_height = height_map[cur_pos] + 1
    for _ in _DIRS:
        new_pos = _shift(cur_pos, _)
        if new_pos in height_map and height_map[new_pos] == new_height:
            yield new_pos


def _count_trailheads_a(height_map: HeightMap, start_pos: Pos) -> int:
    res = 0
    visited = set()
    assert height_map[start_pos] == 0
    active = [start_pos]
    while active:
        cur_pos = active.pop()
        visited.add(cur_pos)
        if height_map[cur_pos] == 9:
            res += 1
            continue
        for new_pos in _gen_positions(cur_pos, height_map):
            if new_pos not in visited:
                active.append(new_pos)
    return res


def _count_trailheads_b(height_map: HeightMap, start_pos: Pos) -> int:
    res = 0
    assert height_map[start_pos] == 0
    active: list[tuple[Pos, tuple[Pos, ...]]] = [(start_pos, (start_pos,))]
    while active:
        cur_pos, cur_path = active.pop()
        if height_map[cur_pos] == 9:
            res += 1
            continue
        for new_pos in _gen_positions(cur_pos, height_map):
            new_path = cur_path + (new_pos,)
            active.append((new_pos, new_path))
    return res


def _get_solve(
    count_trailheads: typing.Callable[[HeightMap, Pos], int]
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        height_map, starts = _parse_input(in_str)
        return sum(count_trailheads(height_map, _) for _ in starts)

    return _solve


solve_a = _get_solve(_count_trailheads_a)
solve_b = _get_solve(_count_trailheads_b)
