MAX_HEIGHT = 9


def calculate_product_of_largest_basins(filename: str) -> int:
    basin_sizes = []
    height_map = read_height_map(filename)
    for (row, column, point) in parse_height_map(height_map):
        try:
            raise_if_not_lower(height_map, row, column - 1, point)
            raise_if_not_lower(height_map, row - 1, column, point)
            raise_if_not_lower(height_map, row, column + 1, point)
            raise_if_not_lower(height_map, row + 1, column, point)
        except ValueError:
            continue

        basin_sizes.append(get_basin_size(height_map, (row, column)))

    basin_sizes.sort(reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


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


def get_basin_size(
    height_map: list[str],
    low_point_coordinates: tuple[int, int],
) -> int:
    coordinates_in_basin: set[tuple[int, int]] = set()
    explore_basin(height_map, low_point_coordinates, coordinates_in_basin)
    return len(coordinates_in_basin)


def explore_basin(
    height_map: list[str],
    target_coordinates: tuple[int, int],
    coordinates_in_basin: set[tuple[int, int]],
) -> None:
    if target_coordinates in coordinates_in_basin:
        return

    target_row, target_column = target_coordinates
    if target_row < 0 or target_column < 0:
        return

    try:
        target_point = int(height_map[target_row].strip()[target_column])
        if target_point == MAX_HEIGHT:
            return
    except IndexError:
        return

    coordinates_in_basin.add(target_coordinates)
    explore_basin(height_map, (target_row, target_column - 1), coordinates_in_basin)
    explore_basin(height_map, (target_row - 1, target_column), coordinates_in_basin)
    explore_basin(height_map, (target_row, target_column + 1), coordinates_in_basin)
    explore_basin(height_map, (target_row + 1, target_column), coordinates_in_basin)


print(calculate_product_of_largest_basins("input.txt"))
