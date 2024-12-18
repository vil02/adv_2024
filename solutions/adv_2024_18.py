import typing
import heapq

Pair = tuple[int, int]

START_POS = (0, 0)
END_POS = (70, 70)
LIMITS = (71, 71)
TRUNC = 1024


def _parse_line(in_line: str) -> Pair:
    x_pos, y_pos = in_line.split(",")
    return int(x_pos), int(y_pos)


def parse_input(in_str: str) -> list[Pair]:
    return [_parse_line(_) for _ in in_str.splitlines()]


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_DIR_TO_NAME = {
    _N: "N",
    _S: "S",
    _W: "W",
    _E: "E",
}

_DIRS = list(_DIR_TO_NAME.keys())


def _shift(in_pos: Pair, shift: Pair) -> Pair:
    _x, _y = in_pos
    _sx, _sy = shift
    res = _x + _sx, _y + _sy
    return res


def _is_in_limits(in_pos: Pair, limits: Pair) -> bool:
    return all(0 <= _p < _l for _p, _l in zip(in_pos, limits, strict=True))


def _gen_positions(
    walls: set[Pair], limits: Pair, in_pos: Pair
) -> typing.Generator[Pair, None, None]:
    for _ in _DIRS:
        new_pos = _shift(in_pos, _)
        if new_pos not in walls and _is_in_limits(new_pos, limits):
            yield new_pos


def _dijkstra(
    walls: set[Pair], limits: Pair, start: Pair
) -> dict[Pair, tuple[int, Pair | None]]:
    res: dict[Pair, tuple[int, Pair | None]] = {}
    visited: set[Pair] = set()
    active: list[tuple[int, Pair, Pair | None]] = []
    heapq.heappush(active, (0, start, None))
    while active:
        cur_dist, cur_node, prev_node = heapq.heappop(active)
        if cur_node in visited:
            continue
        visited.add(cur_node)
        if cur_node not in res or cur_dist < res[cur_node][0]:
            res[cur_node] = (cur_dist, prev_node)
            for new_pos in _gen_positions(walls, limits, cur_node):
                if new_pos not in visited:
                    heapq.heappush(active, (cur_dist + 1, new_pos, cur_node))
    return res


def _get_shift(prev_pos: Pair, cur_pos: Pair) -> Pair:
    res = cur_pos[0] - prev_pos[0], cur_pos[1] - prev_pos[1]
    assert _shift(prev_pos, res) == cur_pos  # nosec B101
    return res


def _to_move(prev_pos: Pair, cur_pos: Pair) -> str:
    return _DIR_TO_NAME[_get_shift(prev_pos, cur_pos)]


def _reconstruct_path(path_data: dict[Pair, tuple[int, Pair | None]], end: Pair) -> str:
    res = []
    cur_pos = end
    while (prev_pos := path_data[cur_pos][1]) is not None:
        res.append(_to_move(prev_pos, cur_pos))
        cur_pos = prev_pos
    return "".join(res[::-1])


def find_shortest_path(walls: set[Pair], limits: Pair, start: Pair, end: Pair) -> int:
    path_data = _dijkstra(walls, limits, start)
    return len(_reconstruct_path(path_data, end))


def solve_a(in_str: str) -> int:
    return find_shortest_path(
        set(parse_input(in_str)[0:TRUNC]), LIMITS, START_POS, END_POS
    )


def _is_connected(wall_list: list[Pair], limits: Pair, start: Pair, end: Pair) -> bool:
    path_data = _dijkstra(set(wall_list), limits, start)
    return end in path_data


def find_first_blocking(
    wall_list: list[Pair], limits: Pair, start: Pair, end: Pair
) -> Pair:
    left = 0
    right = len(wall_list)
    assert _is_connected(wall_list[0:left], limits, start, end)
    assert not _is_connected(wall_list[0:right], limits, start, end)
    while left + 1 < right:
        mid = left + (right - left) // 2
        if _is_connected(wall_list[0:mid], limits, start, end):
            left = mid
        else:
            right = mid
    return wall_list[mid]


def solve_b(in_str: str) -> str:
    first_blocking = find_first_blocking(
        parse_input(in_str), LIMITS, START_POS, END_POS
    )
    return ",".join(str(_) for _ in first_blocking)
