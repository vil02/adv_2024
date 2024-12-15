import typing

Pair = tuple[int, int]
Map = dict[Pair, str]

_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_MOVE_DICT = {
    ">": _E,
    "<": _W,
    "^": _N,
    "v": _S,
}


def _shift(pos: Pair, shift: Pair) -> Pair:
    return pos[0] + shift[0], pos[1] + shift[1]


_WALL = "#"
_BOX = "O"
_EMPTY = "."


def _parse_map(in_str: str) -> tuple[dict[Pair, str], Pair]:
    res = {}
    lines = in_str.splitlines()
    start_pos = None
    for y_pos, line in enumerate(lines):
        for x_pos, char in enumerate(line):
            if char == "@":
                start_pos = (x_pos, y_pos)
                res[(x_pos, y_pos)] = _EMPTY
            else:
                res[(x_pos, y_pos)] = char
    assert start_pos is not None
    return res, start_pos


def _parse_moves(in_str: str) -> list[Pair]:
    return [_MOVE_DICT[_] for _ in in_str if _ in _MOVE_DICT]


def _parse_input(in_str: str) -> tuple[Map, Pair, list[Pair]]:
    map_str, moves_str = in_str.split("\n\n")
    map_data, start_pos = _parse_map(map_str)
    return map_data, start_pos, _parse_moves(moves_str)


def _can_be_moved(in_map: Map, pos: Pair, in_dir: Pair) -> bool:
    assert in_map[pos] == _BOX
    new_pos = _shift(pos, in_dir)
    if in_map[new_pos] == _EMPTY:
        return True
    if in_map[new_pos] == _WALL:
        return False
    assert in_map[new_pos] == _BOX
    return _can_be_moved(in_map, new_pos, in_dir)


def _move_box(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    assert mut_map[pos] == _BOX
    next_pos = _shift(pos, in_dir)
    if mut_map[next_pos] == _EMPTY:
        mut_map[next_pos] = _BOX
        mut_map[pos] = _EMPTY
        return
    assert mut_map[next_pos] == _BOX
    mut_map[pos] = _EMPTY
    _move_box(mut_map, next_pos, in_dir)
    mut_map[next_pos] = _BOX


def _move_robot_a(mut_map: Map, robot_pos: Pair, in_dir: Pair) -> Pair:
    next_robot_pos = _shift(robot_pos, in_dir)
    if mut_map[next_robot_pos] == _EMPTY:
        return next_robot_pos
    if mut_map[next_robot_pos] == _BOX and _can_be_moved(
        mut_map, next_robot_pos, in_dir
    ):
        _move_box(mut_map, next_robot_pos, in_dir)
        return next_robot_pos
    return robot_pos


def _get_make_all_moves(
    move_robot: typing.Callable[[Map, Pair, Pair], Pair]
) -> typing.Callable[[Map, Pair, list[Pair]], None]:
    def _make_all_moves(mut_map: Map, robot_pos: Pair, moves: list[Pair]) -> None:
        cur_robot_pos = robot_pos
        for _ in moves:
            cur_robot_pos = move_robot(mut_map, cur_robot_pos, _)

    return _make_all_moves


_make_all_moves_a = _get_make_all_moves(_move_robot_a)


def _single_gps(pos: Pair) -> int:
    pos_x, pos_y = pos
    return 100 * pos_y + pos_x


def _gps(in_map: Map) -> int:
    return sum(_single_gps(_k) for _k, _v in in_map.items() if _v == _BOX)


def solve_a(in_str: str) -> int:
    mut_map, start_pos, moves = _parse_input(in_str)
    _make_all_moves_a(mut_map, start_pos, moves)
    return _gps(mut_map)


def _widen(in_str: str) -> str:
    res = in_str
    res = res.replace("#", "##")
    res = res.replace("O", "[]")
    res = res.replace(".", "..")
    res = res.replace("@", "@.")
    return res


def _is_box(in_map: Map, pos: Pair) -> bool:
    return in_map[pos] == "[" or in_map[pos] == "]"


_HOR_DIRS = {_E, _W}
_VER_DIRS = {_N, _S}


def _can_be_moved_horizontally(in_map: Map, pos: Pair, in_dir: Pair) -> bool:
    assert in_dir in _HOR_DIRS
    assert _is_box(in_map, pos)

    new_pos = _shift(pos, in_dir)
    if in_map[new_pos] == _EMPTY:
        return True
    if in_map[new_pos] == _WALL:
        return False
    assert _is_box(in_map, new_pos)
    return _can_be_moved_horizontally(in_map, new_pos, in_dir)


def _box_dir(in_map: Map, pos: Pair) -> Pair:
    assert _is_box(in_map, pos)
    if in_map[pos] == "[":
        return _E
    assert in_map[pos] == "]"
    return _W


def _can_be_moved_vertically(in_map: Map, pos: Pair, in_dir: Pair) -> bool:
    assert in_dir in _VER_DIRS
    assert _is_box(in_map, pos)
    new_pos_a, new_pos_b = _box_pos_after_vertical_shift(in_map, pos, in_dir)
    if in_map[new_pos_a] == _EMPTY and in_map[new_pos_b] == _EMPTY:
        return True
    if _WALL in (in_map[new_pos_a], in_map[new_pos_b]):
        return False
    if in_map[new_pos_a] == _EMPTY and _is_box(in_map, new_pos_b):
        return _can_be_moved_vertically(in_map, new_pos_b, in_dir)
    if _is_box(in_map, new_pos_a) and in_map[new_pos_b] == _EMPTY:
        return _can_be_moved_vertically(in_map, new_pos_a, in_dir)
    assert _is_box(in_map, new_pos_a)
    assert _is_box(in_map, new_pos_b)
    return _can_be_moved_vertically(
        in_map, new_pos_a, in_dir
    ) and _can_be_moved_vertically(in_map, new_pos_b, in_dir)


def _can_be_moved_b(in_map: Map, pos: Pair, in_dir: Pair) -> bool:
    if in_dir in _HOR_DIRS:
        return _can_be_moved_horizontally(in_map, pos, in_dir)
    return _can_be_moved_vertically(in_map, pos, in_dir)


def _upcoming_positions(pos: Pair, in_dir: Pair) -> tuple[Pair, Pair]:
    next_pos = _shift(pos, in_dir)
    next_next_pos = _shift(next_pos, in_dir)
    return next_pos, next_next_pos


def _move_single_box_horizontally(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    next_pos, next_next_pos = _upcoming_positions(pos, in_dir)
    mut_map[next_next_pos] = mut_map[next_pos]
    mut_map[next_pos] = mut_map[pos]
    mut_map[pos] = _EMPTY


def _move_horizontally(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    assert in_dir in _HOR_DIRS
    assert _is_box(mut_map, pos)
    next_pos, next_next_pos = _upcoming_positions(pos, in_dir)
    assert _is_box(mut_map, next_pos)
    if mut_map[next_next_pos] == _EMPTY:
        _move_single_box_horizontally(mut_map, pos, in_dir)
        return
    _move_horizontally(mut_map, next_next_pos, in_dir)
    _move_single_box_horizontally(mut_map, pos, in_dir)


def _box_positions(in_map: Map, pos: Pair) -> tuple[Pair, Pair]:
    assert _is_box(in_map, pos)
    box_dir = _box_dir(in_map, pos)
    other_pos = _shift(pos, box_dir)
    if pos < other_pos:
        return pos, other_pos
    return other_pos, pos


def _box_pos_after_vertical_shift(
    in_map: Map, pos: Pair, in_dir: Pair
) -> tuple[Pair, Pair]:
    pos_a, pos_b = _box_positions(in_map, pos)
    return _shift(pos_a, in_dir), _shift(pos_b, in_dir)


def _move_single_box_vertically(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    assert _is_box(mut_map, pos)
    pos_a, pos_b = _box_positions(mut_map, pos)
    new_pos_a, new_pos_b = _box_pos_after_vertical_shift(mut_map, pos, in_dir)
    mut_map[new_pos_a] = mut_map[pos_a]
    mut_map[pos_a] = _EMPTY
    mut_map[new_pos_b] = mut_map[pos_b]
    mut_map[pos_b] = _EMPTY


def _move_vertically(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    pos_a, _ = _box_positions(mut_map, pos)
    new_pos_a, new_pos_b = _box_pos_after_vertical_shift(mut_map, pos_a, in_dir)
    if mut_map[new_pos_a] == _EMPTY and mut_map[new_pos_b] == _EMPTY:
        _move_single_box_vertically(mut_map, pos_a, in_dir)
        return
    if mut_map[new_pos_a] == _EMPTY and _is_box(mut_map, new_pos_b):
        _move_vertically(mut_map, new_pos_b, in_dir)
        _move_single_box_vertically(mut_map, pos_a, in_dir)
        return
    if mut_map[new_pos_b] == _EMPTY and _is_box(mut_map, new_pos_a):
        _move_vertically(mut_map, new_pos_a, in_dir)
        _move_single_box_vertically(mut_map, pos_a, in_dir)
        return
    assert _is_box(mut_map, new_pos_a)
    assert _is_box(mut_map, new_pos_b)
    _move_vertically(mut_map, new_pos_a, in_dir)
    if _is_box(mut_map, new_pos_b):
        _move_vertically(mut_map, new_pos_b, in_dir)
    _move_single_box_vertically(mut_map, pos_a, in_dir)


def _move_box_b(mut_map: Map, pos: Pair, in_dir: Pair) -> None:
    if in_dir in _HOR_DIRS:
        _move_horizontally(mut_map, pos, in_dir)
        return
    assert in_dir in _VER_DIRS
    assert _can_be_moved_vertically(mut_map, pos, in_dir)
    _move_vertically(mut_map, pos, in_dir)


def _move_robot_b(mut_map: Map, robot_pos: Pair, in_dir: Pair) -> Pair:
    next_robot_pos = _shift(robot_pos, in_dir)
    if mut_map[next_robot_pos] == _EMPTY:
        return next_robot_pos
    if _is_box(mut_map, next_robot_pos) and _can_be_moved_b(
        mut_map, next_robot_pos, in_dir
    ):
        _move_box_b(mut_map, next_robot_pos, in_dir)
        return next_robot_pos
    return robot_pos


_make_all_moves_b = _get_make_all_moves(_move_robot_b)


def _gps_b(in_map: Map) -> int:
    return sum(_single_gps(_k) for _k, _v in in_map.items() if _v == "[")


def solve_b(in_str: str) -> int:
    mut_map, start_pos, moves = _parse_input(_widen(in_str))
    _make_all_moves_b(mut_map, start_pos, moves)
    return _gps_b(mut_map)
