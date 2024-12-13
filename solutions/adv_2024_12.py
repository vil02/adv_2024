import typing
import math

Pos = tuple[int, int]
Garden = dict[Pos, str]
Region = set[Pos]


def _shift(pos: Pos, shift: Pos) -> Pos:
    return pos[0] + shift[0], pos[1] + shift[1]


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)


_DIRS = (_N, _S, _W, _E)
assert len(set(_DIRS)) == 4


_NW = _shift(_N, _W)
_NE = _shift(_N, _E)
_SW = _shift(_S, _W)
_SE = _shift(_S, _E)

_COMPS = {
    _NW: [_N, _W],
    _SW: [_S, _W],
    _NE: [_N, _E],
    _SE: [_S, _E],
}


def _parse_input(in_str: str) -> Garden:
    res = {}
    lines = in_str.splitlines()
    for y_pos, line in enumerate(lines):
        for x_pos, char in enumerate(line):
            res[(x_pos, y_pos)] = char
    return res


def _full_region(garden: Garden, start_pos: Pos) -> Region:
    visited = set()
    active = [start_pos]
    while active:
        cur_pos = active.pop()
        if cur_pos in visited:
            continue
        visited.add(cur_pos)
        for new_pos in (_shift(cur_pos, _) for _ in _DIRS):
            if garden.get(new_pos, "") == garden[start_pos] and new_pos not in visited:
                active.append(new_pos)
    return visited


def _area(region: Region) -> int:
    return len(region)


def _count_visited_neighbors(visited: Region, pos: Pos) -> int:
    return sum(1 for cur_dir in _DIRS if _shift(pos, cur_dir) in visited)


def _perimeter(region: Region) -> int:
    res = 0
    visited: Region = set()
    for _ in region:
        res_change = {0: 4, 1: 2, 2: 0, 3: -2, 4: -4}
        res += res_change[_count_visited_neighbors(visited, _)]
        visited.add(_)
    return res


def _is_convex_corner(region: Region, pos: Pos, in_dir: Pos) -> bool:
    assert pos in region
    return all(_shift(pos, _) not in region for _ in _COMPS[in_dir])


def _is_concave_corner(region: Region, pos: Pos, in_dir: Pos) -> bool:
    assert pos in region
    if _shift(pos, in_dir) in region:
        return False
    return all(_shift(pos, _) in region for _ in _COMPS[in_dir])


def _is_corner(region: Region, pos: Pos, in_dir: Pos) -> bool:
    return _is_concave_corner(region, pos, in_dir) or _is_convex_corner(
        region, pos, in_dir
    )


def _count_corners_at_pos(region: Region, pos: Pos) -> int:
    return sum(1 for cur_dir in _COMPS if _is_corner(region, pos, cur_dir))


def _corners(region: Region) -> int:
    return sum(_count_corners_at_pos(region, _) for _ in region)


def _compute_components(garden: Garden) -> list[Region]:
    start_positions = set(garden.keys())
    res = []
    while start_positions:
        cur_start = next(iter(start_positions))
        cur_component = _full_region(garden, cur_start)
        res.append(cur_component)
        assert cur_component <= start_positions
        start_positions -= cur_component
    return res


Cost = typing.Callable[[Region], int]


def _cost_of_region(costs: list[Cost], region: Region) -> int:
    res = math.prod(_(region) for _ in costs)
    assert isinstance(res, int)
    return res


def _get_solve(costs: list[Cost]) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        return sum(
            _cost_of_region(costs, _) for _ in _compute_components(_parse_input(in_str))
        )

    return _solve


solve_a = _get_solve([_area, _perimeter])
solve_b = _get_solve([_area, _corners])
