import asyncio

import numpy

Area = tuple[tuple[str]]


def read(filename: str) -> Area:
    area = []
    with open(filename, "r") as input_file:
        for line in input_file:
            area.append(tuple(line.strip()))
    return area


async def move_until_stop(area: Area) -> None:
    steps = 0
    while True:
        previous_area = area
        area = await move_east(area)
        area = await move_south(area)
        steps += 1
        if previous_area == area:
            break
    print(steps)


async def move_east(area: Area) -> Area:
    tasks = []
    for line in area:
        tasks.append(move(line, ">"))
    return tuple(await asyncio.gather(*tasks))


async def move_south(area: Area) -> Area:
    tasks = []
    rotated_area = numpy.rot90(area)
    for line in rotated_area:
        tasks.append(move(line, "v"))
    return tuple(map(tuple, numpy.rot90(await asyncio.gather(*tasks), k=-1)))


async def move(line: tuple[str], target: str) -> tuple[str]:
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
asyncio.run(move_until_stop(area))
