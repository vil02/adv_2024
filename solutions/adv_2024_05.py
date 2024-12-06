import collections


def _parse_order_rule(in_str: str) -> tuple[int, int]:
    lo, hi = in_str.split("|")
    return int(lo), int(hi)


def _parse_rules(in_str: str) -> dict[int, set[int]]:
    res = collections.defaultdict(set)
    for _ in in_str.splitlines():
        lo, hi = _parse_order_rule(_)
        res[lo].add(hi)
    return res


def _parse_pages(in_str: str) -> list[int]:
    return [int(_) for _ in in_str.split(",")]


def _parse_all_pages(in_str: str) -> list[list[int]]:
    return [_parse_pages(_) for _ in in_str.splitlines()]


def _parse_input(in_str: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    rules, all_pages = in_str.split("\n\n")

    return _parse_rules(rules), _parse_all_pages(all_pages)


def _is_correct(in_pages: list[int], in_rules: dict[int, set[int]]) -> bool:
    pages_set = set(in_pages)
    page_to_ind = {_p: _i for _i, _p in enumerate(in_pages)}
    for cur_ind, cur_page in enumerate(in_pages):
        pages_after = in_rules.get(cur_page, set()) & pages_set
        if any(page_to_ind[hi] < cur_ind for hi in pages_after):
            return False
    return True


def _get_middle_page(in_pages: list[int]) -> int:
    assert len(in_pages) % 2 == 1
    return in_pages[len(in_pages) // 2]


def solve_a(in_str: str) -> int:
    rules, all_pages = _parse_input(in_str)
    return sum(_get_middle_page(_) for _ in all_pages if _is_correct(_, rules))


def _relevant_rules(pages: set[int], rules: dict[int, set[int]]) -> dict[int, set[int]]:
    return {_: rules[_] & pages for _ in pages & set(rules.keys())}


def _successors(rules: dict[int, set[int]]) -> set[int]:
    res = set()
    for _ in rules.values():
        res.update(_)
    return res


def _has_processors(in_page: int, rules: dict[int, set[int]]) -> bool:
    return any(in_page in successors for successors in rules.values())


def _remove_successors_and_update_active(
    rules: dict[int, set[int]], active: set[int], cur_page: int
) -> None:
    if cur_page in rules:
        for other_page in list(rules[cur_page]):
            rules[cur_page].remove(other_page)
            if not _has_processors(other_page, rules):
                active.add(other_page)


def _sort(in_pages: list[int], all_rules: dict[int, set[int]]) -> list[int]:
    pages_set = set(in_pages)
    rules = _relevant_rules(set(pages_set), all_rules)

    active = pages_set - _successors(rules)
    res = []
    while active:
        cur_page = active.pop()
        res.append(cur_page)
        _remove_successors_and_update_active(rules, active, cur_page)

    assert set(res) == pages_set
    assert _is_correct(res, all_rules)
    assert not any(rules.values())
    return res


def solve_b(in_str: str) -> int:
    rules, all_pages = _parse_input(in_str)
    return sum(
        _get_middle_page(_sort(_, rules))
        for _ in all_pages
        if not _is_correct(_, rules)
    )
