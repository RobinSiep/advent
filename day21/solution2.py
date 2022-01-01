from itertools import product
from typing import Optional

played_games = {}

POSSIBLE_ROLLS: list[tuple[int, int, int]] = list(
    product(*[list(range(1, 4)) for _ in range(3)])
)


class Player:
    id_: int
    score: int
    position: int

    def __init__(self, id_: int, position: int, score: int = 0) -> None:
        self.id_ = id_
        self.position = position
        self.score = score

    def __repr__(self) -> str:
        return f"{self.id_} {self.position} {self.score}"

    def __hash__(self) -> int:
        return hash((self.position, self.score))

    def __eq__(self, other: any) -> bool:
        return hash(self) == hash(other)


class Game:
    players: list[Player]

    def __init__(self, players: list[Player], observed_player_id: int = 0) -> None:
        self.players = players
        self.observed_player_id = observed_player_id

    def play(self) -> int:
        posibilities = 0
        player = self.players[0]
        for roll in POSSIBLE_ROLLS:
            total_roll = sum(roll)
            new_game = self.move(player, total_roll)
            cached = played_games.get(new_game)

            if winner := new_game.get_winner():
                posibilities += int(winner.id_ == self.observed_player_id)
            elif cached is not None:
                posibilities += cached
            else:
                posibilities += new_game.play()

        played_games[self] = posibilities
        return posibilities

    def move(self, player: Player, amount: int):
        position = player.position
        new_position = (position + amount) % 10
        new_position = 10 if new_position == 0 else new_position
        new_players = [
            self.players[1],
            Player(player.id_, new_position, player.score + new_position),
        ]
        return Game(new_players, self.observed_player_id)

    def get_winner(self) -> Optional[Player]:
        for player in self.players:
            if player.score >= 21:
                return player

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __eq__(self, other: any) -> bool:
        return hash(self) == hash(other)

    def __repr__(self) -> str:
        return " - ".join([player.__repr__() for player in self.players])


def read_players(filename: str) -> list[Player]:
    players = []
    with open(filename, "r") as input_file:
        for i, line in enumerate(input_file):
            _, starting_position_str = line.strip().split(":")
            players.append(Player(i, int(starting_position_str.strip())))

    return players


players = read_players("input.txt")
game = Game(players, 1)
posibilities = game.play()
print(posibilities)
