from statistics import median


def calculate_fuel_cost(horizontal_positions: list[int], median_position: int) -> int:
    fuel_cost = 0
    for position in horizontal_positions:
        fuel_cost += abs(median_position - position)

    return fuel_cost


def read_horizontal_positions(filename: str) -> list[int]:
    with open(filename, "r") as input_file:
        line = input_file.readline()
        return [int(position) for position in line.strip().split(",")]


horizontal_positions = read_horizontal_positions("input.txt")
median_position = int(median(horizontal_positions))
fuel_cost = calculate_fuel_cost(horizontal_positions, median_position)
print(fuel_cost)
