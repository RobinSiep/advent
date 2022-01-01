from contextlib import contextmanager
from typing import ContextManager

from z3 import Optimize, BitVec, BitVecVal, And, If, sat

ZERO = BitVecVal(0, 64)
ONE = BitVecVal(1, 64)
DIGITS_BASE_10 = BitVec("DIGITS_BASE_10", 64)


class IntVar:
    solver: Optimize
    value: BitVecVal = ZERO

    def __init__(self, solver: Optimize) -> None:
        self.solver = solver

    def inp(self, a: int, i: int) -> None:
        self.value = a

    def add(self, b: int, i: int) -> None:
        value = self._new_value(i)
        self.solver.add(value == self.value + b)
        self.value = value

    def mul(self, b: int, i: int) -> None:
        value = self._new_value(i)
        self.solver.add(value == self.value * b)
        self.value = value

    def div(self, b: int, i: int) -> None:
        value = self._new_value(i)
        self.solver.add(b != 0)
        self.solver.add(value == self.value / b)
        self.value = value

    def mod(self, b: int, i: int) -> None:
        value = self._new_value(i)
        self.solver.add(self.value >= 0)
        self.solver.add(b > 0)
        self.solver.add(value == self.value % b)
        self.value = value

    def eql(self, b: int, i: int) -> None:
        value = self._new_value(i)
        self.solver.add(value == If(self.value == b, ONE, ZERO))
        self.value = value

    def _new_value(self, i: int) -> BitVec:
        return BitVec(f"value_{i}", 64)


class Program:
    solver: Optimize
    register: dict[str, IntVar]
    remaining_input: list[BitVec]

    def __init__(self) -> None:
        self.remaining_input = [BitVec(f"digit_{i}", 64) for i in range(14)]
        solver = self._create_solver()
        self.register = {
            "w": IntVar(solver),
            "x": IntVar(solver),
            "y": IntVar(solver),
            "z": IntVar(solver),
        }
        self.solver = solver

    def _create_solver(self) -> Optimize:
        solver = Optimize()
        for digit in self.remaining_input:
            solver.add(And(digit >= 1, digit <= 9))

        solver.add(
            DIGITS_BASE_10
            == sum((10**i) * d for i, d in enumerate(self.remaining_input[::-1]))
        )
        return solver

    def execute(self, instruction: tuple, i: int):
        function = instruction[0]
        target = self.register[instruction[1]]
        try:
            arg = instruction[2]
            if isinstance(arg, str):
                arg = self.register[arg].value
        except IndexError:
            arg = self.remaining_input.pop(0)
        getattr(target, function)(arg, i)

    @contextmanager
    def run(self) -> ContextManager[Optimize]:
        for i, instruction in enumerate(instructions):
            self.execute(instruction, i)
        self.solver.add(self.register["z"].value == 0)
        self.solver.push()
        yield self.solver
        self.solver.pop()


def read(filename: str) -> tuple[tuple]:
    instructions = []
    with open(filename, "r") as input_file:
        for line in input_file:
            instruction = line.strip().split(" ")
            for i in range(1, len(instruction)):
                try:
                    instruction[i] = int(instruction[i])
                except ValueError:
                    continue
            instructions.append(tuple(instruction))
        return tuple(instructions)


def find_largest(instructions: tuple[tuple]) -> int:
    program = Program()
    with program.run() as solver:
        solver.maximize(DIGITS_BASE_10)
        assert solver.check() == sat
        return solver.model().eval(DIGITS_BASE_10)


instructions = read("input.txt")
print(find_largest(instructions))
