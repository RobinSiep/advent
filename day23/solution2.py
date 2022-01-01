from heapq import heappop, heappush
from typing import Optional


energy_costs = {"A": 1, "B": 10, "C": 100, "D": 1000}
room_to_hall = {"A": 2, "B": 4, "C": 6, "D": 8}
valid_pos = (0, 1, 3, 5, 7, 9, 10)
empty = "."

State = tuple[str, ...]


def read(filename: str) -> State:
    hallway = []
    amphipods = []
    with open(filename, "r") as input_file:
        for line in input_file:
            for c in line:
                if c == empty:
                    hallway.append(c)
                elif c.isalpha():
                    amphipods.append(c)

    return (*hallway, *amphipods)


def get_target_state(initial_state: State) -> State:
    amphipods = [pos for pos in initial_state if pos != empty]
    target_amphipods = [[None] * 4 for i in range(int(len(amphipods) / 4))]
    for amphipod in amphipods:
        room = ord(amphipod) - 65
        for level in target_amphipods:
            if level[room] is None:
                level[room] = amphipod
                break
    return (
        *[pos for pos in initial_state if pos == empty],
        *[amphipod for room in target_amphipods for amphipod in room],
    )


def can_leave_room(state: State, room_pos: range) -> Optional[int]:
    for a in room_pos:
        if state[a] == empty:
            continue
        return a


def blocked(from_: int, to: int, state: State) -> bool:
    step = 1 if from_ < to else -1
    for pos in range(from_, to, step):
        if state[pos + step] != empty:
            return True
    return False


def get_possible_valid_pos(from_: int, state: State) -> Optional[int]:
    for to in [pos for pos in valid_pos if state[pos] == empty]:
        if blocked(from_, to, state):
            continue
        yield to


def move(from_: int, to: int, state: State) -> State:
    new_state = list(state)
    new_state[from_], new_state[to] = new_state[to], new_state[from_]
    return tuple(new_state)


def can_enter_room(
    from_: int, to: int, amphi: str, state: State, room_pos: range
) -> int | bool:
    for pos in room_pos:
        if state[pos] == empty:
            best_pos = pos
        elif state[pos] != amphi:
            return False
    if not blocked(from_, to, state):
        return best_pos


def possible_moves(state: State, target: dict[str, range]) -> tuple[int, int]:
    for from_ in [pos for pos in valid_pos if state[pos] != empty]:
        amphi = state[from_]
        if to := can_enter_room(
            from_, room_to_hall[amphi], amphi, state, target[amphi]
        ):
            yield from_, to
    for room in "ABCD":
        if not (from_ := can_leave_room(state, target[room])):
            continue
        for to in get_possible_valid_pos(room_to_hall[room], state):
            yield from_, to


def calculate_least_energy(initial_state: State, target_state: State) -> int:
    target = {r: range(ord(r) - 54, len(initial_state), 4) for r in "ABCD"}
    target_i = {v: key for key, val in target.items() for v in val}

    heap, seen = [(0, initial_state)], {initial_state: 0}
    while heap:
        cost, state = heappop(heap)
        if state == target_state:
            return cost
        for from_, to in possible_moves(state, target):
            distance = calculate_distance(target_i, from_, to)
            new_cost = cost + distance * energy_costs[state[from_]]
            moved = move(from_, to, state)
            if seen.get(moved, 999999) <= new_cost:
                continue
            seen[moved] = new_cost
            heappush(heap, (new_cost, moved))


def calculate_distance(target_i: dict[int, str], from_: int, to: int) -> int:
    p, r = (from_, to) if from_ < to else (to, from_)
    return abs(room_to_hall[target_i[r]] - p) + (r - 7) // 4


initial_state = read("input2.txt")
print(calculate_least_energy(initial_state, get_target_state(initial_state)))
