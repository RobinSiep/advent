import pprint
from itertools import product

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
        if low > 50 or high < -50:
            return None

        boundaries.append((low, high))
    return boundaries


def compute(insructions: list[Instruction]) -> set[tuple[int, int, int]]:
    on_cubes = set()
    for on, boundaries in instructions:
        for cube in get_cuboid(boundaries):
            if on:
                on_cubes.add(cube)
            else:
                try:
                    on_cubes.remove(cube)
                except KeyError:
                    pass
    return on_cubes


def get_cuboid(
    boundaries: tuple[Boundary, Boundary, Boundary]
) -> set[tuple[int, int, int]]:
    return set(product(*(range(low, high + 1) for low, high in boundaries)))


instructions = read("input.txt")
on_cubes = compute(instructions)
pprint.pprint(len(on_cubes))
