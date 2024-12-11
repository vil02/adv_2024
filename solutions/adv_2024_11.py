import functools
import typing


def _parse_input(in_str: str) -> list[int]:
    return [int(_) for _ in in_str.split()]


@functools.lru_cache(maxsize=None)
def _number_of_stones_produced(in_num: int, number_of_blinks: int) -> int:
    assert number_of_blinks >= 0
    if number_of_blinks == 0:
        return 1
    if in_num == 0:
        return _number_of_stones_produced(1, number_of_blinks - 1)
    num_str = str(in_num)
    if len(num_str) % 2 == 0:
        num_a = int(num_str[0 : len(num_str) // 2])
        num_b = int(num_str[len(num_str) // 2 :])
        return _number_of_stones_produced(
            num_a, number_of_blinks - 1
        ) + _number_of_stones_produced(num_b, number_of_blinks - 1)
    return _number_of_stones_produced(2024 * in_num, number_of_blinks - 1)


def number_of_stones_produced(stones: list[int], number_of_blinks: int) -> int:
    return sum(_number_of_stones_produced(_, number_of_blinks) for _ in stones)


def _get_solve(number_of_blinks: int) -> typing.Callable[[str], int]:
    def _solve(in_str: str) -> int:
        return number_of_stones_produced(_parse_input(in_str), number_of_blinks)

    return _solve


solve_a = _get_solve(25)
solve_b = _get_solve(75)
