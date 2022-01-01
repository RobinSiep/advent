import numpy

Area = tuple[tuple[str, ...], ...]


def read(filename: str) -> Area:
    area = []
    with open(filename, "r") as input_file:
        for line in input_file:
            area.append(tuple(line.strip()))
    return tuple(area)


def move_until_stop(area: Area) -> None:
    steps = 0
    while True:
        previous_area = area
        area = move_east(area)
        area = move_south(area)
        steps += 1
        if previous_area == area:
            break
    print(steps)


def move_east(area: Area) -> Area:
    return tuple(move(line, ">") for line in area)


def move_south(area: Area) -> Area:
    rotated_area = numpy.rot90(area)
    moved = tuple(move(tuple(line), "v") for line in rotated_area)
    return tuple(map(tuple, numpy.rot90(moved, k=-1)))


def move(line: tuple[str, ...], target: str) -> tuple[str, ...]:
    new_line = list(line)
    length = len(line)
    last_i = length - 1
    i = 0
    while i <= last_i:
        char = line[i]
        new_char = char
        increment = 1
        if i == last_i:
            next_i = 0
        else:
            next_i = i + 1
        next_char = line[next_i]
        if next_char == "." and char == target:
            new_char = "."
            new_line[next_i] = char
            increment = 2
        new_line[i] = new_char
        i += increment
    return tuple(new_line)


area = read("input.txt")
move_until_stop(area)
