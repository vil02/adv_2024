def _parse_register(in_str: str, reg_name: str) -> int:
    assert in_str.startswith("Register " + reg_name)
    _, register_str = in_str.split(": ")
    return int(register_str)


def _parse_program(in_str: str) -> list[int]:
    prefix = "Program: "
    assert in_str.startswith(prefix)
    nums = in_str.removeprefix(prefix).split(",")
    assert len(nums) % 2 == 0
    return [int(_) for _ in nums]


def _parse_input(in_str: str) -> tuple[int, int, int, list[int]]:
    registers, program = in_str.split("\n\n")
    register_a, register_b, register_c = registers.splitlines()

    return (
        _parse_register(register_a, "A"),
        _parse_register(register_b, "B"),
        _parse_register(register_c, "C"),
        _parse_program(program),
    )


class Computer:
    def __init__(self, in_a: int, in_b: int, in_c: int, instructions: list[int]):
        self._a: int = in_a
        self._b: int = in_b
        self._c: int = in_c
        self._instructions: list[int] = instructions
        self._output: list[int] = []
        self._cur_instruction: int = 0

    def _operand_value(self, operand: int) -> int:
        assert 0 <= operand < 7
        if operand < 4:
            return operand
        return {4: self._a, 5: self._b, 6: self._c}[operand]

    def _incr_cur_instruction(self) -> None:
        self._cur_instruction += 2

    def _divide(self, operand: int) -> int:
        res = self._a // 2 ** self._operand_value(operand)
        assert isinstance(res, int)
        return res

    def _adv(self, operand: int) -> None:
        self._a = self._divide(operand)
        self._incr_cur_instruction()

    def _blx(self, operand: int) -> None:
        self._b = self._b ^ operand
        self._incr_cur_instruction()

    def _bst(self, operand: int) -> None:
        self._b = self._operand_value(operand) % 8
        self._incr_cur_instruction()

    def _jnz(self, operand: int) -> None:
        if self._a != 0 and self._cur_instruction != operand:
            self._cur_instruction = operand
        else:
            self._incr_cur_instruction()

    def _bcx(self, _: int) -> None:
        self._b = self._b ^ self._c
        self._incr_cur_instruction()

    def _out(self, operand: int) -> None:
        self._output.append(self._operand_value(operand) % 8)
        self._incr_cur_instruction()

    def _bdv(self, operand: int) -> None:
        self._b = self._divide(operand)
        self._incr_cur_instruction()

    def _cdv(self, operand: int) -> None:
        self._c = self._divide(operand)
        self._incr_cur_instruction()

    def _compute(self, opcode: int, operand: int) -> None:
        assert self._cur_instruction % 2 == 0
        assert 0 <= self._cur_instruction < len(self._instructions) - 1
        {
            0: self._adv,
            1: self._blx,
            2: self._bst,
            3: self._jnz,
            4: self._bcx,
            5: self._out,
            6: self._bdv,
            7: self._cdv,
        }[opcode](operand)

    def compute_all(self) -> list[int]:
        while self._cur_instruction < len(self._instructions):
            self._compute(
                self._instructions[self._cur_instruction],
                self._instructions[self._cur_instruction + 1],
            )
        return self._output

    def get_state(self) -> tuple[int, int, int, list[int]]:
        return self._a, self._b, self._c, self._output


def _compute_output(
    reg_a: int, reg_b: int, reg_c: int, program: list[int]
) -> list[int]:
    computer = Computer(reg_a, reg_b, reg_c, program)
    return computer.compute_all()


def solve_a(in_str: str) -> str:
    reg_a, reg_b, reg_c, program = _parse_input(in_str)
    res = _compute_output(reg_a, reg_b, reg_c, program)
    return ",".join(str(_) for _ in res)


def _find_reg_a(reg_b: int, reg_c: int, program: list[int]) -> int:
    active = [0]
    for cur_len in range(1, len(program) + 1):
        old_active = active
        active = []
        for cur in old_active:
            for digit in range(8):
                reg_a = 8 * cur + digit
                if _compute_output(reg_a, reg_b, reg_c, program) == program[-cur_len:]:
                    active.append(reg_a)
    return min(active)


def solve_b(in_str: str) -> int:
    _, reg_b, reg_c, program = _parse_input(in_str)
    return _find_reg_a(reg_b, reg_c, program)
