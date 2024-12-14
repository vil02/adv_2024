import typing

Pair = tuple[int, int]
Region = set[Pair]


def _parse_pair(in_str: str) -> Pair:
    x_str, y_str = in_str[2:].split(",")
    return int(x_str), int(y_str)


def _parse_line(in_line: str) -> tuple[Pair, Pair]:
    pos_str, vel_str = in_line.split(" ")
    return _parse_pair(pos_str), _parse_pair(vel_str)


def _parse_input(in_str: str) -> list[tuple[Pair, Pair]]:
    return [_parse_line(_) for _ in in_str.splitlines()]


def _to_positions_and_vels(
    data: list[tuple[Pair, Pair]]
) -> tuple[list[Pair], list[Pair]]:
    positions = [_[0] for _ in data]
    vels = [_[1] for _ in data]
    return positions, vels


def _shift(pos: Pair, shift: Pair) -> Pair:
    return pos[0] + shift[0], pos[1] + shift[1]


def _wrap_coordinate(value: int, limit: int) -> int:
    return value % limit


def _wrap(pos: Pair, limits: Pair) -> Pair:
    return _wrap_coordinate(pos[0], limits[0]), _wrap_coordinate(pos[1], limits[1])


def _move(pos: Pair, vel: Pair, limits: Pair) -> Pair:
    return _wrap(_shift(pos, vel), limits)


def _move_all(positions: list[Pair], vels: list[Pair], limits: Pair) -> list[Pair]:
    return [_move(_p, _v, limits) for _p, _v in zip(positions, vels, strict=True)]


def _simulate_all(
    positions: list[Pair], vels: list[Pair], limits: Pair, steps: int
) -> list[Pair]:
    res = positions
    for _ in range(steps):
        res = _move_all(res, vels, limits)
    return res


def _count(positions: list[Pair], condition: typing.Callable[[Pair], bool]) -> int:
    return sum(1 for _ in positions if condition(_))


def _safety_factor(positions: list[Pair], limits: Pair) -> int:
    mid_x = limits[0] // 2
    mid_y = limits[1] // 2

    def _is_in_0(pos: Pair) -> bool:
        return 0 <= pos[0] < mid_x and 0 <= pos[1] < mid_y

    def _is_in_1(pos: Pair) -> bool:
        return mid_x < pos[0] and 0 <= pos[1] < mid_y

    def _is_in_2(pos: Pair) -> bool:
        return 0 <= pos[0] < mid_x and mid_y < pos[1]

    def _is_in_3(pos: Pair) -> bool:
        return mid_x < pos[0] and mid_y < pos[1]

    return (
        _count(positions, _is_in_0)
        * _count(positions, _is_in_1)
        * _count(positions, _is_in_2)
        * _count(positions, _is_in_3)
    )


_LIMITS = (101, 103)


def solve_a(in_str: str) -> int:
    positions, vels = _to_positions_and_vels(_parse_input(in_str))
    positions = _simulate_all(positions, vels, _LIMITS, 100)
    return _safety_factor(positions, _LIMITS)


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)
_DIRS = (_N, _S, _W, _E)


def _full_region(positions_set: Region, start_pos: Pair) -> Region:
    visited = set()
    active = [start_pos]
    while active:
        cur_pos = active.pop()
        if cur_pos in visited:
            continue
        visited.add(cur_pos)
        for new_pos in (_shift(cur_pos, _) for _ in _DIRS):
            if new_pos in positions_set and new_pos not in visited:
                active.append(new_pos)
    return visited


def _compute_components(positions_set: Region) -> list[Region]:
    start_positions = set(positions_set)
    res = []
    while start_positions:
        cur_start = next(iter(start_positions))
        cur_component = _full_region(positions_set, cur_start)
        res.append(cur_component)
        assert cur_component <= start_positions
        start_positions -= cur_component
    return res


def _max_cluster_size(positions: list[Pair]) -> int:
    return max(len(_) for _ in _compute_components(set(positions)))


def solve_b(in_str: str) -> int:
    positions, vels = _to_positions_and_vels(_parse_input(in_str))
    move = 0
    while _max_cluster_size(positions) < 20:
        positions = _move_all(positions, vels, _LIMITS)
        move += 1
    return move
