from typing import Optional

Boundary = tuple[int, int]
Instruction = tuple[bool, tuple[Boundary, Boundary, Boundary]]


def read(filename: str) -> list[Instruction]:
    instructions = []
    with open(filename, "r") as input_file:
        for line in input_file:
            line = line.strip()
            state, boundary_strings = line.split(" ")
            state = state == "on"
            boundaries = read_boundaries(boundary_strings)
            if boundaries is None:
                continue

            instructions.append((state, tuple(boundaries)))

    return instructions


def read_boundaries(boundary_strings: str) -> list[Boundary]:
    boundaries = []
    for boundary_string in boundary_strings.split(","):
        low, high = [int(boundary) for boundary in boundary_string[2:].split("..")]
        boundaries.append((low, high))
    return boundaries


def compute_complete_instruction_set(
    instructions: list[Instruction],
) -> list[Instruction]:
    previous_instructions = []
    for instruction in instructions:
        to_add = [instruction] if instruction[0] else []
        for previous_instruction in previous_instructions:
            intersection = get_intersection(instruction, previous_instruction)
            if intersection:
                to_add += [intersection]
        previous_instructions += to_add
    return previous_instructions


def get_intersection(one: Instruction, other: Instruction) -> Optional[Instruction]:
    _, (x, y, z) = one
    other_state, (other_x, other_y, other_z) = other
    intersecting_boundaries = (
        get_overlap(x, other_x),
        get_overlap(y, other_y),
        get_overlap(z, other_z),
    )
    if None in intersecting_boundaries:
        return None
    return (not other_state, intersecting_boundaries)


def get_overlap(one: Boundary, other: Boundary) -> Optional[Boundary]:
    start, end = (max(one[0], other[0]), min(one[1], other[1]))
    if start > end:
        return None
    return (start, end)


def count_on_cubes(instructions: list[Instruction]) -> int:
    on = 0
    for instruction in instructions:
        state, ((low_x, high_x), (low_y, high_y), (low_z, high_z)) = instruction
        modifier = 1 if state else -1
        on += (
            (high_x - low_x + 1)
            * (high_y - low_y + 1)
            * (high_z - low_z + 1)
            * modifier
        )
    return on


initial_instructions = read("input.txt")
instructions = compute_complete_instruction_set(initial_instructions)
print(count_on_cubes(instructions))
