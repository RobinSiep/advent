from typing import Optional, TextIO


class Number:
    value: int
    marked: bool

    def __init__(self, value: int) -> None:
        self.value = value
        self.marked = False

    def __repr__(self) -> str:
        return f"{self.value} {self.marked}"


class Board:
    rows: list[list[int]]

    def __init__(self, rows: list[list[int]]) -> None:
        self.rows = rows

    def mark(self, value: int) -> None:
        for row in self.rows:
            for number in row:
                if number.value == value:
                    number.marked = True

    def check_for_winner(self) -> bool:
        for row in self.rows:
            if all([number.marked for number in row]):
                return True

        # rotate
        for row in list(zip(*self.rows[::-1])):
            if all([number.marked for number in row]):
                return True

    def calculate_score(self, draw: int) -> int:
        total_sum = 0
        for row in self.rows:
            for number in row:
                if number.marked:
                    continue

                total_sum += number.value

        return total_sum * draw


class Game:
    boards: list[Board]
    draws = list[int]

    def __init__(self, boards: list[Board], draws: list[int]):
        self.boards = boards
        self.draws = draws

    def find_winning_score(self) -> Optional[int]:
        for draw in self.draws:
            for board in self.boards:
                board.mark(draw)

                if board.check_for_winner():
                    return board.calculate_score(draw)


def read(filename: str) -> tuple[list[Board], list[int]]:
    draws: list[int] = []
    boards: list[Board] = []

    with open(filename, "r") as input_file:
        draws = parse_draws(next(input_file))
        next(input_file)
        while True:
            board = read_board(input_file)
            if not board:
                return (boards, draws)

            boards.append(board)


def parse_draws(line: str) -> list[int]:
    return [int(draw) for draw in line.split(",")]


def read_board(input_file: TextIO) -> Optional[Board]:
    rows: list[list[int]] = []
    while line := next(input_file, "").strip():
        rows.append([Number(int(val)) for val in line.split(" ") if val.strip() != ""])

    if not rows:
        return None

    return Board(rows)


boards, draws = read("input.txt")
game = Game(boards, draws)
print(game.find_winning_score())
