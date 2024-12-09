import typing

_EMPTY = -1


def _parse_input(in_str: str) -> str:
    return in_str.strip()


def _get_free_space(in_str: str, pos: int) -> int:
    assert 0 <= pos <= len(in_str)
    if pos < len(in_str):
        return int(in_str[pos])
    return 0


def _is_empty(data: list[int], pos: int) -> bool:
    return data[pos] == _EMPTY


def to_blocks(in_str: str) -> list[int]:
    res: list[int] = []
    for file_id in range(len(in_str) // 2 + 1):
        block_number = int(in_str[2 * file_id])
        res += [file_id for _ in range(block_number)]
        res += [_EMPTY for _ in range(_get_free_space(in_str, 2 * file_id + 1))]
    return res


def _find_first_free(data: list[int], search_start: int) -> int:
    pos = search_start
    while pos < len(data) and not _is_empty(data, pos):
        pos += 1
    return pos


def _find_last_used(data: list[int], search_start: int) -> int:
    cur_pos = search_start
    while cur_pos >= 0:
        if not _is_empty(data, cur_pos):
            return cur_pos
        cur_pos -= 1
    return cur_pos


def _move_piece(data: list[int], used_pos: int, free_pos: int) -> None:
    assert not _is_empty(data, used_pos)
    assert _is_empty(data, free_pos)
    data[free_pos] = data[used_pos]
    data[used_pos] = _EMPTY


def _move_a(data: list[int]) -> None:
    last_pos = _find_last_used(data, len(data) - 1)
    first_free = _find_first_free(data, 0)
    while first_free < last_pos:
        _move_piece(data, last_pos, first_free)
        last_pos = _find_last_used(data, last_pos - 1)
        first_free = _find_first_free(data, first_free + 1)


def _checksum(data: list[int]) -> int:
    return sum(id * val for id, val in enumerate(data) if not _is_empty(data, id))


class _Blocks:
    def __init__(self, in_raw: list[int]) -> None:
        self._raw = in_raw
        self._empty: set[int] = {
            _ for _ in range(len(self._raw)) if _is_empty(self._raw, _)
        }

    def move_piece(self, used_pos: int, free_pos: int) -> None:
        _move_piece(self._raw, used_pos, free_pos)
        self._empty.remove(free_pos)
        self._empty.add(used_pos)

    def move_file(self, file_start: int, file_size: int, dest_start: int) -> None:
        for _ in range(file_size):
            self.move_piece(file_start + _, dest_start + _)

    def find_last_used(self, search_start: int) -> int:
        return _find_last_used(self._raw, search_start)

    def file_begin(self, end_pos: int) -> int:
        cur_pos = end_pos
        assert not _is_empty(self._raw, cur_pos)
        while self._raw[cur_pos] == self._raw[end_pos]:
            cur_pos -= 1
        return cur_pos + 1

    def find_free_big_enough(self, size: int, search_end: int) -> int:
        for cur_pos in sorted(_ for _ in self._empty if _ < search_end):
            if _get_free_space_size(self._raw, cur_pos) >= size:
                assert isinstance(cur_pos, int)
                return cur_pos
        return len(self._raw)


def _get_free_space_size(data: list[int], pos: int) -> int:
    assert _is_empty(data, pos)
    size = 0
    while pos < len(data) and _is_empty(data, pos):
        size += 1
        pos += 1
    return size


def _move_b(data: list[int]) -> None:
    blocks = _Blocks(data)
    end_pos = blocks.find_last_used(len(data) - 1)
    while end_pos > 0:
        start_pos = blocks.file_begin(end_pos)
        file_size = end_pos - start_pos + 1
        free_pos = blocks.find_free_big_enough(file_size, start_pos)
        if free_pos < start_pos:
            blocks.move_file(start_pos, file_size, free_pos)

        end_pos = blocks.find_last_used(start_pos - 1)


def _get_solve(move: typing.Callable[[list[int]], None]) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        data = to_blocks(_parse_input(in_str))
        move(data)
        return _checksum(data)

    return _solve


solve_a = _get_solve(_move_a)
solve_b = _get_solve(_move_b)
