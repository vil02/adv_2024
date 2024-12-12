import typing

Pos = tuple[int, int]
Garden = dict[Pos, str]


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


def _expand_pos(in_pos: Pos) -> Pos:
    return 2 * in_pos[0], 2 * in_pos[1]


def _get_all_edges(in_pos: Pos) -> list[frozenset[Pos]]:
    pos = _expand_pos(in_pos)
    ne = _shift(pos, _NE)
    nw = _shift(pos, _NW)
    se = _shift(pos, _SE)
    sw = _shift(pos, _SW)

    return [
        frozenset({ne, nw}),
        frozenset({nw, sw}),
        frozenset({sw, se}),
        frozenset({se, ne}),
    ]


def _full_region(garden: Garden, start_pos: Pos) -> set[Pos]:
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


def _find_area(garden: Garden, start_pos: Pos) -> int:
    return len(_full_region(garden, start_pos))


def _find_all_edges(garden: Garden, start_pos: Pos) -> set[frozenset[Pos]]:
    edges_count: dict[frozenset[Pos], int] = {}

    for _ in _full_region(garden, start_pos):
        for edge in _get_all_edges(_):
            edges_count[edge] = edges_count.get(edge, 0) + 1

    return {_k for _k, _v in edges_count.items() if _v == 1}


def _find_perimeter(garden: Garden, start_pos: Pos) -> int:
    return len(_find_all_edges(garden, start_pos))


def _get_at_shifted(garden: Garden, pos: Pos, in_dir: Pos) -> str:
    return garden.get(_shift(pos, in_dir), "")


def _is_convex_corner(garden: Garden, pos: Pos, in_dir: Pos) -> bool:
    cur_char = garden[pos]
    return all(_get_at_shifted(garden, pos, _) != cur_char for _ in _COMPS[in_dir])


def _is_concave_corner(garden: Garden, pos: Pos, in_dir: Pos) -> bool:
    cur_char = garden[pos]
    if _get_at_shifted(garden, pos, in_dir) == cur_char:
        return False
    return all(_get_at_shifted(garden, pos, _) == cur_char for _ in _COMPS[in_dir])


def _is_corner(garden: Garden, pos: Pos, in_dir: Pos) -> bool:
    return _is_concave_corner(garden, pos, in_dir) or _is_convex_corner(
        garden, pos, in_dir
    )


def _count_corners_at_pos(garden: Garden, pos: Pos) -> int:
    return sum(1 for cur_dir in _COMPS if _is_corner(garden, pos, cur_dir))


def _find_corners(garden: Garden, start_pos: Pos) -> int:
    return sum(
        _count_corners_at_pos(garden, _) for _ in _full_region(garden, start_pos)
    )


def _compute_components(garden: Garden) -> list[set[Pos]]:
    start_positions = set(garden.keys())
    res = []
    while start_positions:
        cur_start = next(iter(start_positions))
        cur_component = _full_region(garden, cur_start)
        res.append(cur_component)
        assert cur_component <= start_positions
        start_positions -= cur_component
    return res


def _get_solve(
    other_cost: typing.Callable[[Garden, Pos], int]
) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        garden = _parse_input(in_str)
        res = 0
        for _ in _compute_components(garden):
            some_node = _.pop()
            res += _find_area(garden, some_node) * other_cost(garden, some_node)
        return res

    return _solve


solve_a = _get_solve(_find_perimeter)
solve_b = _get_solve(_find_corners)
