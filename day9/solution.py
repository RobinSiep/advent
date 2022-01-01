def calculate_risk_level_of_height_map(filename: str) -> int:
    risk_level = 0
    height_map = read_height_map(filename)
    for (row, column, point) in parse_height_map(height_map):
        try:
            raise_if_not_lower(height_map, row, column - 1, point)
            raise_if_not_lower(height_map, row - 1, column, point)
            raise_if_not_lower(height_map, row, column + 1, point)
            raise_if_not_lower(height_map, row + 1, column, point)
        except ValueError:
            continue

        risk_level += point + 1
    return risk_level


def read_height_map(filename: str) -> tuple[int, int, int]:
    with open(filename, "r") as input_file:
        return input_file.readlines()


def parse_height_map(height_map: list[str]) -> tuple[int, int, int]:
    for row, line in enumerate(height_map):
        line = line.strip()
        for column, point in enumerate(line):
            yield (row, column, int(point))


def raise_if_not_lower(
    height_map: list[str],
    row: int,
    column: int,
    target_point: int,
) -> None:
    try:
        if row < 0 or column < 0:
            raise IndexError

        if target_point >= int(height_map[row].strip()[column]):
            raise ValueError
    except IndexError:
        return


risk_level = calculate_risk_level_of_height_map("input.txt")
print(risk_level)
