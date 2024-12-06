Pair = tuple[int, int]
SetPairs = set[Pair]


def _parse_input(in_str: str) -> tuple[SetPairs, Pair, Pair]:
    res = set()
    guard_pos = None
    lines = in_str.splitlines()
    size_y = len(lines)
    size_x = len(lines[0])
    for y_pos, line in enumerate(lines):
        assert size_x == len(line)
        for x_pos, char in enumerate(line):
            if char == "#":
                res.add((x_pos, y_pos))
            elif char == "^":
                assert guard_pos is None
                guard_pos = (x_pos, y_pos)
    assert guard_pos is not None
    return res, guard_pos, (size_x, size_y)


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_ROTATED = {_N: _E, _E: _S, _S: _W, _W: _N}
_DIRS = list(_ROTATED.keys())


def _is_on(pos: Pair, limits: Pair) -> bool:
    return 0 <= pos[0] < limits[0] and 0 <= pos[1] < limits[1]


def _shift(pos: Pair, shift: Pair) -> Pair:
    return pos[0] + shift[0], pos[1] + shift[1]


def _move(walls: SetPairs, pos: Pair, in_dir: Pair) -> tuple[Pair, Pair]:
    assert pos not in walls
    if _shift(pos, in_dir) in walls:
        return pos, _ROTATED[in_dir]
    return _shift(pos, in_dir), in_dir


def _simulate(walls: SetPairs, pos: Pair, in_dir: Pair, limits: Pair) -> set[Pair]:
    visited = set()
    cur_pos = pos
    cur_dir = in_dir
    while _is_on(cur_pos, limits):
        visited.add(cur_pos)
        cur_pos, cur_dir = _move(walls, cur_pos, cur_dir)
    return visited


def solve_a(in_str: str) -> int:
    walls, start_pos, limits = _parse_input(in_str)
    return len(_simulate(walls, start_pos, _N, limits))


def _does_loop(walls: SetPairs, pos: Pair, in_dir: Pair, limits: Pair) -> bool:
    cur_pos = pos
    cur_dir = in_dir
    _visited_states = {(cur_pos, cur_dir)}
    while _is_on(cur_pos, limits):
        cur_pos, cur_dir = _move(walls, cur_pos, cur_dir)
        if (cur_pos, cur_dir) in _visited_states:
            return True
        _visited_states.add((cur_pos, cur_dir))
    return False


def _get_potential(visited: SetPairs, walls: SetPairs, limits: Pair) -> SetPairs:
    res = set()
    for _p in visited:
        for _d in _DIRS:
            pos = _shift(_p, _d)
            if _is_on(pos, limits) and pos not in walls:
                res.add(pos)
    return res


def solve_b(in_str: str) -> int:
    walls, start_pos, limits = _parse_input(in_str)
    tmp = _simulate(walls, start_pos, _N, limits)
    potential = _get_potential(tmp, walls, limits)
    return sum(
        1
        for _ in potential - {start_pos}
        if _does_loop(walls | {_}, start_pos, _N, limits)
    )
