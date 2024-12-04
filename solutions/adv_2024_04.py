import itertools

Pos = tuple[int, int]
Words = dict[Pos, str]


def _parse_input(in_str: str) -> tuple[Words, int, int]:
    res = {}
    lines = in_str.splitlines()
    y_size = len(lines)
    x_size = len(lines[0])
    for y_pos, line in enumerate(lines):
        assert x_size == len(line)
        for x_pos, char in enumerate(line):
            res[(x_pos, y_pos)] = char
    return res, x_size, y_size


_N = (0, -1)
_S = (0, 1)
_W = (-1, 0)
_E = (1, 0)

_NE = (1, -1)
_NW = (-1, -1)
_SE = (1, 1)
_SW = (-1, 1)

_DIRS = (_N, _S, _W, _E, _NE, _NW, _SE, _SW)
assert len(set(_DIRS)) == 8


def _shift(pos: Pos, shift: Pos) -> Pos:
    return pos[0] + shift[0], pos[1] + shift[1]


def _is_at_pos_in_dir(words: Words, pos: Pos, search_dir: Pos, in_word: str) -> bool:
    cur_pos = pos
    for char in in_word:
        if words.get(cur_pos, "") != char:
            return False
        cur_pos = _shift(cur_pos, search_dir)
    return True


def _count_at_pos(words: Words, pos: Pos, in_word: str) -> int:
    return sum(1 for _ in _DIRS if _is_at_pos_in_dir(words, pos, _, in_word))


def solve_a(in_str: str) -> int:
    data, x_size, y_size = _parse_input(in_str)
    return sum(
        _count_at_pos(data, _, "XMAS")
        for _ in itertools.product(range(x_size), range(y_size))
    )


_NEG_DDIR = {
    _NE: _SW,
    _SW: _NE,
    _NW: _SE,
    _SE: _NW,
}

_ROTATE_DDIR = {
    _NW: _SW,
    _NE: _NW,
    _SE: _NE,
    _SW: _SE,
}


def _is_x_mas(words: Words, pos: Pos) -> bool:
    _mas = "MAS"
    for first, second in _ROTATE_DDIR.items():
        if _is_at_pos_in_dir(
            words, _shift(pos, first), _NEG_DDIR[first], _mas
        ) and _is_at_pos_in_dir(words, _shift(pos, second), _NEG_DDIR[second], _mas):
            return True
    return False


def solve_b(in_str: str) -> int:
    words, x_size, y_size = _parse_input(in_str)
    return sum(
        1
        for _ in itertools.product(range(x_size), range(y_size))
        if _is_x_mas(words, _)
    )
