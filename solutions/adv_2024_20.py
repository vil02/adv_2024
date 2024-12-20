import typing

Pair = tuple[int, int]


def _parse_input(in_str: str, wall: str = "#") -> tuple[set[Pair], Pair, Pair]:
    walls: set[Pair] = set()
    start = None
    end = None
    lines = in_str.splitlines()
    for y_pos, line in enumerate(lines):
        for x_pos, _ in enumerate(line):
            if _ == wall:
                walls.add((x_pos, y_pos))
            elif _ == "S":
                assert start is None
                start = (x_pos, y_pos)
            elif _ == "E":
                assert end is None
                end = (x_pos, y_pos)
    assert start is not None
    assert end is not None
    return walls, start, end


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_DIRS = [_N, _S, _W, _E]


def _shift(in_pos: Pair, shift: Pair) -> Pair:
    _x, _y = in_pos
    _sx, _sy = shift
    return _x + _sx, _y + _sy


def _gen_positions(
    walls: set[Pair], in_pos: Pair
) -> typing.Generator[Pair, None, None]:
    for _ in _DIRS:
        new_pos = _shift(in_pos, _)
        if new_pos not in walls:
            yield new_pos


def _new_paths(
    walls: set[Pair], visited: set[Pair], cur_path: list[Pair]
) -> list[list[Pair]]:
    cur_pos = cur_path[-1]
    return [
        cur_path + [new_pos]
        for new_pos in _gen_positions(walls, cur_pos)
        if new_pos not in visited
    ]


def _optimal_path(walls: set[Pair], start: Pair, end: Pair) -> list[Pair] | None:
    """it is assumed that the maze has no loops"""
    visited = set()
    active = [[start]]
    while active:
        cur_path = active.pop()
        cur_pos = cur_path[-1]
        if cur_pos == end:
            return cur_path
        assert cur_pos not in visited
        visited.add(cur_pos)
        active += _new_paths(walls, visited, cur_path)
    return None


def _dist(pos_a: Pair, pos_b: Pair) -> int:
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def _count_cheats(pos_path: list[Pair], cheat_size: int) -> int:
    res = 0
    for ind_a, pos_a in enumerate(pos_path):
        for ind_b in range(ind_a + 102, len(pos_path)):
            dist = _dist(pos_a, pos_path[ind_b])
            if (ind_b - ind_a) - dist >= 100 and dist <= cheat_size:
                res += 1

    return res


def _get_solve(cheat_size: int) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        walls, start, end = _parse_input(in_str)
        pos_path = _optimal_path(walls, start, end)
        assert pos_path is not None
        assert pos_path[0] == start
        assert pos_path[-1] == end
        return _count_cheats(pos_path, cheat_size)

    return _solve


solve_a = _get_solve(2)
solve_b = _get_solve(20)
