import typing
import heapq

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


def _gen_positions(
    walls: set[Pair], in_pos: Pair
) -> typing.Generator[Pair, None, None]:
    for _ in _DIRS:
        new_pos = _shift(in_pos, _)
        if new_pos not in walls:
            yield new_pos


def _dijkstra(walls: set[Pair], start: Pair) -> dict[Pair, tuple[int, Pair | None]]:
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
            for new_pos in _gen_positions(walls, cur_node):
                if new_pos not in visited:
                    heapq.heappush(active, (cur_dist + 1, new_pos, cur_node))
    return res


def _reconstruct_path(
    path_data: dict[Pair, tuple[int, Pair | None]], end: Pair
) -> list[Pair]:
    res = [end]
    cur_pos = end
    while (prev_pos := path_data[cur_pos][1]) is not None:
        res.append(prev_pos)
        cur_pos = prev_pos
    return res[::-1]


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
        path_data = _dijkstra(walls, start)
        pos_path = _reconstruct_path(path_data, end)
        assert pos_path[0] == start
        assert pos_path[-1] == end
        return _count_cheats(pos_path, cheat_size)

    return _solve


solve_a = _get_solve(2)
solve_b = _get_solve(20)
