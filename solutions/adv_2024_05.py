def _parse_order_rule(in_str: str) -> tuple[int, int]:
    lo, hi = in_str.split("|")
    return int(lo), int(hi)


def _parse_rules(in_str: str) -> dict[int, set[int]]:
    raw = [_parse_order_rule(_) for _ in in_str.splitlines()]
    res = {}
    for lo, hi in raw:
        if lo not in res:
            res[lo] = {hi}
        else:
            res[lo].add(hi)
    return res


def _parse_pages(in_str: str) -> list[int]:
    res = [int(_) for _ in in_str.split(",")]
    assert len(res) % 2 == 1
    return res


def _parse_all_pages(in_str: str) -> list[list[int]]:
    return [_parse_pages(_) for _ in in_str.splitlines()]


def _parse_input(in_str: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    rules, all_pages = in_str.split("\n\n")

    return _parse_rules(rules), _parse_all_pages(all_pages)


def _is_correct(in_pages: list[int], in_rules: dict[int, set[int]]) -> bool:
    pages_set = set(in_pages)
    for cur_pos, cur_page in enumerate(in_pages):
        if cur_page in in_rules and any(
            in_pages.index(hi) < cur_pos
            for hi in in_rules[cur_page].intersection(pages_set)
        ):
            return False
    return True


def _get_middle_page(in_pages: list[int]) -> int:
    assert len(in_pages) % 2 == 1
    return in_pages[len(in_pages) // 2]


def solve_a(in_str: str) -> int:
    rules, all_pages = _parse_input(in_str)
    return sum(_get_middle_page(_) for _ in all_pages if _is_correct(_, rules))


def _sort(in_pages: list[int], tmp_in_rules: dict[int, set[int]]) -> list[int]:
    in_rules = {
        _k: tmp_in_rules[_k].intersection(in_pages)
        for _k in set(in_pages).intersection(set(tmp_in_rules.keys()))
    }

    all_nodes = set(in_pages)
    nodes_with_incoming_edges = set()
    for successors in in_rules.values():
        nodes_with_incoming_edges.update(successors)

    active = all_nodes - nodes_with_incoming_edges
    res = []
    while active:
        n = active.pop()
        res.append(n)

        if n in in_rules:
            for m in list(in_rules[n]):
                in_rules[n].remove(m)
                has_incoming_edges = any(
                    m in successors for successors in in_rules.values()
                )
                if not has_incoming_edges:
                    active.add(m)

    assert set(res) == set(in_pages)
    assert _is_correct(res, tmp_in_rules)
    assert not any(in_rules.values())
    return res


def solve_b(in_str: str) -> int:
    rules, all_pages = _parse_input(in_str)
    return sum(
        _get_middle_page(_sort(_, rules))
        for _ in all_pages
        if not _is_correct(_, rules)
    )
