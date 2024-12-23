import networkx  # type: ignore


def _parse_input(in_str: str) -> networkx.Graph:
    res = networkx.Graph()
    for _ in in_str.splitlines():
        node_a, node_b = _.split("-")
        res.add_edge(node_a, node_b)
    return res


def _is_chief_historian(in_list: list[str]) -> bool:
    return any(_.startswith("t") for _ in in_list)


def solve_a(in_str: str) -> int:
    return sum(
        1
        for _ in networkx.simple_cycles(_parse_input(in_str), 3)
        if _is_chief_historian(_)
    )


def solve_b(in_str: str) -> str:
    max_clique = max(networkx.find_cliques(_parse_input(in_str)), key=len)
    return ",".join(sorted(max_clique))
