import pytest

import solutions.adv_2024_21 as sol
from . import test_utils as tu


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [
        ("A", "A", {""}),
        ("A", "3", {"^"}),
        ("5", "9", {">^", "^>"}),
        ("3", "4", {"<<^", "<^<", "^<<"}),
        ("9", "1", {"<<vv", "vv<<", "<v<v", "v<v<", "<vv<", "v<<v"}),
    ],
)
def test_numeric_keypad_sequences(start: str, end: str, expected: set[str]) -> None:
    assert sol.numeric_keypad_sequences(start, end) == expected


@pytest.mark.parametrize(
    ("start", "end", "expected"),
    [
        ("A", "A", {""}),
        ("<", "v", {">"}),
        ("<", "^", {">^"}),
        ("<", "A", {">>^", ">^>"}),
        ("A", "v", {"<v", "v<"}),
        ("A", "<", {"<v<", "v<<"}),
    ],
)
def test_directional_keypad_sequences(start: str, end: str, expected: set[str]) -> None:
    assert sol.directional_keypad_sequences(start, end) == expected


@pytest.mark.parametrize(
    ("keys", "expected"),
    [
        ("029A", {"<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"}),
    ],
)
def test_numeric_keypad_press_sequence(keys: str, expected: set[str]) -> None:
    assert sol.numeric_keypad_press_sequence(keys) == expected


@pytest.mark.parametrize(
    ("code", "iter_size", "expected"),
    [
        (
            "029A",
            2,
            len("<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"),
        ),
        (
            "980A",
            2,
            len("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A"),
        ),
        (
            "179A",
            2,
            len("<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
        ),
        (
            "456A",
            2,
            len("<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A"),
        ),
        (
            "379A",
            2,
            len("<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A"),
        ),
    ],
)
def test_shortest_full_sequence_press(code: str, iter_size: int, expected: int) -> None:
    assert sol.shortest_full_sequence_press(code, iter_size) == expected


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("029A", 29),
        ("980A", 980),
        ("179A", 179),
        ("456A", 456),
        ("379A", 379),
    ],
)
def test_numeric_part(code: str, expected: int) -> None:
    assert sol.numeric_part(code) == expected


_INPUTS = tu.get_inputs(21, {"small", "p"})

test_solve_a, test_solve_b = _INPUTS.get_tests(
    (sol.solve_a, sol.solve_b),
    {"small": (126384, 154115708116294), "p": (278568, 341460772681012)},
)
