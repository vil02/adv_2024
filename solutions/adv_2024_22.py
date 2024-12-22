import math
import functools


def _parse_input(in_str: str) -> list[int]:
    return [int(_) for _ in in_str.splitlines()]


def _mix(val: int, secret: int) -> int:
    return val ^ secret


def _prune(val: int) -> int:
    return val % 16777216


def _mix_and_prune(val: int, secret: int) -> int:
    return _prune(_mix(val, secret))


def next_secret(secret: int) -> int:
    secret = _mix_and_prune(secret * 64, secret)
    secret = _mix_and_prune(math.floor(secret / 32), secret)
    return _mix_and_prune(secret * 2048, secret)


@functools.cache
def _all_secrets(secret: int) -> list[int]:
    res = [secret]
    cur_val = secret
    for _ in range(2000):
        cur_val = next_secret(cur_val)
        res.append(cur_val)
    return res


def solve_a(in_str: str) -> int:
    return sum(
        _all_secrets(
            _,
        )[-1]
        for _ in _parse_input(in_str)
    )


def _prices(secret: int) -> list[int]:
    return [_ % 10 for _ in _all_secrets(secret)]


def _changes(prices: list[int]) -> list[int]:
    return [_n - _p for _n, _p in zip(prices[1:], prices)]


def _possible_prices(
    prices: list[int], changes: list[int]
) -> dict[tuple[int, int, int, int], int]:
    res = {}
    for _ in range(len(changes) - 3):
        pattern = (changes[_], changes[_ + 1], changes[_ + 2], changes[_ + 3])
        if pattern not in res:
            res[pattern] = prices[_ + 4]
    return res


def solve_b(in_str: str) -> int:
    results: dict[tuple[int, int, int, int], int] = {}
    for _ in _parse_input(in_str):
        prices = _prices(_)
        for _k, _v in _possible_prices(prices, _changes(prices)).items():
            results[_k] = results.get(_k, 0) + _v
    return max(results.values())
