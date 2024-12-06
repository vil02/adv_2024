Pos = tuple[int, int]
Words = dict[Pos, str]


def _parse_input(in_str: str) -> Words:
    res = {}
    for y_pos, line in enumerate(in_str.splitlines()):
        for x_pos, char in enumerate(line):
            res[(x_pos, y_pos)] = char
    return res


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


def _is_at_pos_in_dir(words: Words, pos: Pos, search_dir: Pos, word: str) -> bool:
    if not word:
        return True
    return words.get(pos, "") == word[0] and _is_at_pos_in_dir(
        words, _shift(pos, search_dir), search_dir, word[1:]
    )


def _count_at_pos(words: Words, pos: Pos, in_word: str) -> int:
    return sum(1 for _ in _DIRS if _is_at_pos_in_dir(words, pos, _, in_word))


def solve_a(in_str: str) -> int:
    words = _parse_input(in_str)
    return sum(_count_at_pos(words, _, "XMAS") for _ in words)


def _is_x_mas(words: Words, pos: Pos) -> bool:
    def _check_diagonal(pos: Pos, shift: Pos) -> bool:
        mas = "MAS"
        return _is_at_pos_in_dir(words, pos, shift, mas) or _is_at_pos_in_dir(
            words, pos, shift, mas[::-1]
        )

    return _check_diagonal(_shift(pos, _NW), _SE) and _check_diagonal(
        _shift(pos, _SW), _NE
    )


def solve_b(in_str: str) -> int:
    words = _parse_input(in_str)
    return sum(1 for _ in words if _is_x_mas(words, _))
