class Octopus:
    energy_level: int
    flashed: bool

    def __init__(self, energy_level: int) -> None:
        self.energy_level = energy_level
        self.flashed = False

    def increase_energy_level(self) -> None:
        self.energy_level = self.energy_level + 1

    def reset(self) -> None:
        self.energy_level = 0
        self.flashed = False


def read(filename: str) -> list[list[Octopus]]:
    octopuses = []
    with open(filename, "r") as input_file:
        for line in input_file:
            line = line.strip()
            octopuses.append([Octopus(int(value)) for value in line])

    return octopuses


def increase_energy_levels(octopuses: list[list[Octopus]]) -> None:
    for row in octopuses:
        for octopus in row:
            octopus.increase_energy_level()


def get_first_simultaneous_flash_step(octopuses: list[list[Octopus]]) -> int:
    max_flash_count = sum([len(row) for row in octopuses])
    step_count = 0
    while True:
        step_count += 1
        increase_energy_levels(octopuses)
        flash_count = simulate_flashes(octopuses)
        if flash_count == max_flash_count:
            return step_count
        reset(octopuses)


def simulate_flashes(octopuses: list[list[Octopus]]) -> int:
    flash_count = 0
    for row_index, row in enumerate(octopuses):
        for column_index, _ in enumerate(row):
            flashed = flash_if_full(octopuses, row_index, column_index)
            if flashed:
                flash_count += 1

    if flash_count:
        flash_count += simulate_flashes(octopuses)

    return flash_count


def flash_if_full(
    octopuses: list[list[Octopus]],
    row_index: int,
    column_index: int,
) -> bool:
    flash = False
    octopus = octopuses[row_index][column_index]
    if octopus.energy_level > 9 and not octopus.flashed:
        flash = True
        octopus.flashed = flash
        increase_energy_levels_for_indices(
            octopuses,
            [
                (row_index, column_index - 1),
                (row_index - 1, column_index - 1),
                (row_index - 1, column_index),
                (row_index - 1, column_index + 1),
                (row_index, column_index + 1),
                (row_index + 1, column_index + 1),
                (row_index + 1, column_index),
                (row_index + 1, column_index - 1),
            ],
        )

    return flash


def increase_energy_levels_for_indices(
    octopuses: list[list[Octopus]],
    indices: list[tuple[int, int]],
) -> None:
    for row_index, column_index in indices:
        if row_index < 0 or column_index < 0:
            continue

        try:
            octopuses[row_index][column_index].increase_energy_level()
        except IndexError:
            continue


def reset(octopuses: list[list[Octopus]]) -> None:
    for row in octopuses:
        for octopus in row:
            if octopus.flashed:
                octopus.reset()


def debug_print(octopuses: list[list[Octopus]]) -> None:
    for row in octopuses:
        print("".join([str(octopus.energy_level) for octopus in row]))


octopuses = read("input.txt")
print(get_first_simultaneous_flash_step(octopuses))
