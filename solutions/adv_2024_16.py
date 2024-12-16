import typing
import heapq
import math
import functools

Pair = tuple[int, int]

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

_NEG_DIR = {_N: _S, _S: _N, _W: _E, _E: _W}


def _parse_input(in_str: str, wall: str = "#") -> tuple[frozenset[Pair], Pair, Pair]:
    walls: set[Pair] = set()
    start = None
    end = None
    for y_pos, line in enumerate(in_str.splitlines()):
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
    return frozenset(walls), start, end


def _shift(in_pos: Pair, shift: Pair) -> Pair:
    _x, _y = in_pos
    _sx, _sy = shift
    res = _x + _sx, _y + _sy
    return res


def _gen_positions(
    walls: set[Pair], in_pos: Pair, last_dir: Pair
) -> typing.Generator[tuple[Pair, Pair], None, None]:
    for new_dir in _DIRS:
        if new_dir != _NEG_DIR[last_dir]:
            new_pos = _shift(in_pos, new_dir)
            if new_pos not in walls:
                yield new_pos, new_dir


def _compute_new_score(cur_score: int, cur_dir: Pair, new_dir: Pair) -> int:
    assert new_dir != _NEG_DIR[cur_dir]
    if cur_dir == new_dir:
        return cur_score + 1
    return cur_score + 1001


@functools.cache
def _find_best_path(
    walls: set[Pair], start: Pair, end: Pair
) -> tuple[int, list[list[Pair]]]:
    best_score = math.inf
    best_paths: list[list[Pair]] = []
    active: list[tuple[int, Pair, Pair, list[Pair]]] = []
    visited: dict[tuple[Pair, Pair], int] = {}
    heapq.heappush(active, (0, start, _E, [start]))
    while active:
        cur_score, cur_pos, cur_dir, cur_path = heapq.heappop(active)
        if cur_score > best_score:
            continue
        if (cur_pos, cur_dir) in visited and visited[(cur_pos, cur_dir)] < cur_score:
            continue
        visited[(cur_pos, cur_dir)] = cur_score
        if cur_pos == end:
            if best_score > cur_score:
                best_score = cur_score
                best_paths = []
            best_paths.append(cur_path)
            continue
        for new_pos, new_dir in _gen_positions(walls, cur_pos, cur_dir):
            heapq.heappush(
                active,
                (
                    _compute_new_score(cur_score, cur_dir, new_dir),
                    new_pos,
                    new_dir,
                    cur_path + [new_pos],
                ),
            )
    assert isinstance(best_score, int)
    return best_score, best_paths


def solve_a(in_str: str) -> int:
    data, start, end = _parse_input(in_str)
    best_score, _ = _find_best_path(data, start, end)
    return best_score


def _get_all_best_tiles(paths: list[list[Pair]]) -> set[Pair]:
    res = set()
    for path in paths:
        res.update(path)
    return res


def solve_b(in_str: str) -> int:
    data, start, end = _parse_input(in_str)
    _, paths = _find_best_path(data, start, end)
    return len(_get_all_best_tiles(paths))
