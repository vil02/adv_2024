Operations = dict[str, tuple[str, str, str]]
Inverted = dict[tuple[str, str, str], str]


def _parse_inputs(in_str: str) -> dict[str, int]:
    res = {}
    for _ in in_str.splitlines():
        wire, value = _.split(": ")
        res[wire] = int(value)
    return res


def _sort_names(wire_a: str, wire_b: str) -> tuple[str, str]:
    res_a, res_b = tuple(sorted([wire_a, wire_b]))
    return res_a, res_b


def _normalise(in_wire_a: str, in_wire_b: str, operation: str) -> tuple[str, str, str]:
    wire_a, wire_b = _sort_names(in_wire_a, in_wire_b)
    return wire_a, wire_b, operation


def _parse_operation(in_line: str) -> tuple[str, str, str, str]:
    args, output_wire = in_line.split(" -> ")
    wire_a, operation, wire_b = args.split()
    return output_wire, wire_a, wire_b, operation


def _parse_operations(in_str: str) -> Operations:
    res: Operations = {}
    for _ in in_str.splitlines():
        output_wire, wire_a, wire_b, operation = _parse_operation(_)
        res[output_wire] = _normalise(wire_a, wire_b, operation)
    return res


def _parse_input(in_str: str) -> tuple[dict[str, int], Operations]:
    inputs, operations = in_str.split("\n\n")
    return _parse_inputs(inputs), _parse_operations(operations)


def _or(val_a: int, val_b: int) -> int:
    return val_a | val_b


def _and(val_a: int, val_b: int) -> int:
    return val_a & val_b


def _xor(val_a: int, val_b: int) -> int:
    return val_a ^ val_b


def _evaluate_operation(operation: str, value_a: int, value_b: int) -> int:
    return {
        "OR": _or,
        "AND": _and,
        "XOR": _xor,
    }[
        operation
    ](value_a, value_b)


def _compute_value(operations: Operations, inputs: dict[str, int], wire: str) -> int:
    if wire in inputs:
        return inputs[wire]
    wire_a, wire_b, operation = operations[wire]
    return _evaluate_operation(
        operation,
        _compute_value(operations, inputs, wire_a),
        _compute_value(operations, inputs, wire_b),
    )


def _output_wires(operations: Operations) -> list[str]:
    return sorted(_ for _ in operations if _.startswith("z"))


def _compute_full_value(operations: Operations, inputs: dict[str, int]) -> int:
    bits = [_compute_value(operations, inputs, _) for _ in _output_wires(operations)]
    bits_str = "".join(str(_) for _ in bits[::-1])
    return int(bits_str, base=2)


def solve_a(in_str: str) -> int:
    inputs, operations = _parse_input(in_str)
    return _compute_full_value(operations, inputs)


def _find_output_wire(
    inverted_operations: Inverted, wire_a: str, wire_b: str, operation: str
) -> str | None:
    return inverted_operations.get(_normalise(wire_a, wire_b, operation), None)


def _name(input_prefix: str, num: int) -> str:
    return input_prefix + str(num).zfill(2)


def _append_not_none(some_list: list[str], new_element: str | None) -> None:
    assert new_element is not None
    some_list.append(new_element)


def _find_all_wires(
    inverted: Inverted, input_num: int, c0: str | None, swapped: list[str]
) -> tuple[str, str]:
    x_input = _name("x", input_num)
    y_input = _name("y", input_num)
    m1 = _find_output_wire(inverted, x_input, y_input, "XOR")
    n1 = _find_output_wire(inverted, x_input, y_input, "AND")

    assert m1 is not None
    assert n1 is not None

    if c0 is not None:
        r1 = _find_output_wire(inverted, c0, m1, "AND")
        if not r1:
            n1, m1 = m1, n1
            _append_not_none(swapped, m1)
            _append_not_none(swapped, n1)
            r1 = _find_output_wire(inverted, c0, m1, "AND")

        z1 = _find_output_wire(inverted, c0, m1, "XOR")

        if m1 and m1.startswith("z"):
            m1, z1 = z1, m1
            _append_not_none(swapped, m1)
            _append_not_none(swapped, z1)

        if n1 and n1.startswith("z"):
            n1, z1 = z1, n1
            _append_not_none(swapped, n1)
            _append_not_none(swapped, z1)

        if r1 and r1.startswith("z"):
            r1, z1 = z1, r1
            _append_not_none(swapped, r1)
            _append_not_none(swapped, z1)

        assert r1 is not None
        assert n1 is not None

        c1 = _find_output_wire(inverted, r1, n1, "OR")
    else:
        z1 = m1
        c1 = n1

    assert z1 is not None
    assert c1 is not None
    return z1, c1


def _invert_operations(operations: Operations) -> Inverted:
    res = {_v: _k for _k, _v in operations.items()}
    assert len(res) == len(operations)
    return res


def solve_b(in_str: str) -> str:
    _, operations = _parse_input(in_str)
    inverted = _invert_operations(operations)
    c0 = None
    swapped: list[str] = []

    input_size = len([_ for _ in operations if _.startswith("z")]) - 2
    for bit_num in range(input_size):
        z1, c1 = _find_all_wires(inverted, bit_num, c0, swapped)

        if c1 and c1.startswith("z") and c1 != _name("z", input_size + 1):
            c1, z1 = z1, c1
            assert c1 is not None
            swapped.append(c1)
            assert z1 is not None
            swapped.append(z1)

        c0 = (
            c1
            if c1
            else _find_output_wire(
                inverted, _name("x", bit_num), _name("y", bit_num), "AND"
            )
        )

    return ",".join(sorted(swapped))
