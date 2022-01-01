def calculate_average(horizontal_positions: list[int]) -> int:
    return int(sum(horizontal_positions) / len(horizontal_positions))


def calculate_fuel_cost(horizontal_positions: list[int], average_position: int) -> int:
    fuel_cost = 0
    for position in horizontal_positions:
        fuel_cost += calculate_triangular_number_distance(average_position, position)

    return fuel_cost


def calculate_triangular_number_distance(
    first_position: int, second_position: int
) -> int:
    steps = abs(first_position - second_position)
    distance = 0
    while steps:
        distance += steps
        steps -= 1

    return distance


def read_horizontal_positions(filename: str) -> list[int]:
    with open(filename, "r") as input_file:
        line = input_file.readline()
        return [int(position) for position in line.strip().split(",")]


horizontal_positions = read_horizontal_positions("input.txt")
average_position = calculate_average(horizontal_positions)
fuel_cost = calculate_fuel_cost(horizontal_positions, average_position)
print(fuel_cost)
