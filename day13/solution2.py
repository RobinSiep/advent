from typing import Optional

Dot = tuple[int, int]
Instruction = tuple[Optional[int], Optional[int]]


def read(filename: str) -> tuple[set[Dot], list[Instruction]]:
    dots = set()
    instructions = []
    with open(filename) as input_file:
        lines = input_file.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                break
            dots.add(tuple((int(value) for value in line.split(","))))

        for line in lines[len(dots) + 1 :]:
            line = line.strip()
            folding_line = int(line.split("=")[1])
            if "x" in line:
                instructions.append((folding_line, None))
            else:
                instructions.append((None, folding_line))

    return dots, instructions


def execute_instructions(dots: set[Dot], instructions: list[Instruction]) -> set[Dot]:
    for instruction in instructions:
        dots = fold(dots, instruction)
    return dots


def fold(dots: set[Dot], instruction: Instruction) -> set[Dot]:
    x, y = instruction
    if x is None:
        return fold_up(dots, y)
    else:
        return fold_left(dots, x)


def fold_up(dots: set[Dot], folding_line: int) -> set[Dot]:
    dots_under_fold = set(dot for dot in dots if dot[1] > folding_line)
    dots_above_fold = dots - dots_under_fold
    new_dots = set()
    for dot in dots_under_fold:
        x, y = dot
        new_dots.add((x, abs(y - folding_line * 2)))

    return set.union(dots_above_fold, new_dots)


def fold_left(dots: set[Dot], folding_line: int) -> set[Dot]:
    dots_right_of_fold = set(dot for dot in dots if dot[0] > folding_line)
    dots_left_of_fold = dots - dots_right_of_fold
    new_dots = set()
    for dot in dots_right_of_fold:
        x, y = dot
        new_dots.add((abs(x - folding_line * 2), y))

    return set.union(dots_left_of_fold, new_dots)


def plot(dots: set[Dot]) -> None:
    paper = []
    max_x = max((dot[0] for dot in dots)) + 1
    max_y = max((dot[1] for dot in dots)) + 1
    for y in range(max_y):
        paper.append([" "] * max_x)

    for dot in dots:
        x, y = dot
        paper[y][x] = 1

    print("\n".join(["".join([str(cell) for cell in row]) for row in paper]))


dots, instructions = read("input.txt")
dots = execute_instructions(dots, instructions)
plot(dots)
