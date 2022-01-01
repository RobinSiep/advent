def read_starting_positions(filename: str) -> list[int]:
    starting_positions = []
    with open(filename, "r") as input_file:
        for line in input_file:
            _, starting_position_str = line.strip().split(":")
            starting_positions.append(int(starting_position_str.strip()))

    return starting_positions


class Game:
    player_count: int
    positions: list[int]
    scores: list[int]
    dice: int = 1
    roll_count: int = 0

    def __init__(self, starting_positions: list[int]) -> None:
        self.player_count = len(starting_positions)
        self.positions = starting_positions
        self.scores = [0] * self.player_count

    def play(self) -> None:
        while True:
            for player in range(self.player_count):
                move_amount = self.roll(3)
                self.move(player, move_amount)
                if self.check_win(player):
                    return

    def roll(self, times: int) -> int:
        total_amount = 0
        for roll in range(times):
            self.roll_count += 1
            total_amount += self.dice
            self.dice += 1
            if self.dice != 100:
                self.dice %= 100

        return total_amount

    def move(self, player: int, amount: int) -> None:
        position = self.positions[player]
        new_position = (position + amount) % 10
        new_position = 10 if new_position == 0 else new_position
        self.positions[player] = new_position
        self.scores[player] += new_position
        print(
            f"player: {player} moves {amount} to {new_position} for total "
            f"score of {self.scores[player]}"
        )

    def check_win(self, player: int) -> bool:
        return self.scores[player] >= 1000


def get_result(game: Game) -> int:
    losing_score = min(game.scores)
    roll_count = game.roll_count
    return losing_score * roll_count


starting_positions = read_starting_positions("input.txt")
game = Game(starting_positions)
game.play()
result = get_result(game)
print(result)
