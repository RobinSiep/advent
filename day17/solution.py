import re
from enum import Enum, auto

MAX_FAILURES_AFTER_SUCCESS = 100

CoordinateRange = tuple[int, int]
Area = tuple[CoordinateRange, CoordinateRange]


class Result(Enum):
    SUCCESS = auto()
    TOO_EARLY = auto()
    TOO_FAR = auto()
    TOO_HIGH = auto()
    TOO_LOW = auto()


def read_target_area(filename: str) -> Area:
    with open(filename, "r") as input_file:
        line = input_file.readlines()[0].strip()
    return find_boundary("x", line), find_boundary("y", line)


def find_boundary(key: str, target_str: str) -> Area:
    regex = f"{key}=-?[0-9]*\.\.-?[0-9]*"  # noqa
    return tuple(
        int(boundary) for boundary in re.findall(regex, target_str)[0][2:].split("..")
    )


def find_highest_y_position(target_area: Area) -> int:
    x_velocity, y_velocity = (0, 0)
    highest_y_position = 0

    while True:
        success_for_x = False
        failures_after_success = 0
        while True:
            velocity = (x_velocity, y_velocity)
            new_highest_y_position, results = fire_probe(velocity, target_area)

            if results == [Result.SUCCESS]:
                success_for_x = True
                failures_after_success = 0
                highest_y_position = max(new_highest_y_position, highest_y_position)
            elif success_for_x:
                failures_after_success += 1

            if Result.TOO_FAR in results and Result.TOO_LOW in results:
                return highest_y_position

            if (
                failures_after_success == MAX_FAILURES_AFTER_SUCCESS
                or Result.TOO_EARLY in results
            ):
                break

            y_velocity += 1

        x_velocity += 1
        y_velocity = 0

    return highest_y_position


def fire_probe(
    initial_velocity: tuple[int, int],
    target_area: Area,
) -> tuple[int, list[Result]]:
    velocity = initial_velocity
    probe_position = [0, 0]
    highest_y_position = 0
    results = []
    step = 0

    while True:
        step += 1
        x_velocity, y_velocity = velocity
        new_position = [probe_position[0] + x_velocity, probe_position[1] + y_velocity]

        probe_position = new_position
        new_x_position, new_y_position = new_position
        highest_y_position = max(highest_y_position, new_y_position)

        if in_target_area(probe_position, target_area):
            results = [Result.SUCCESS]
            break

        y_velocity -= 1
        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1

        velocity = (x_velocity, y_velocity)
        if failure_results := target_area_unreachable(
            probe_position, velocity, target_area
        ):
            results = failure_results
            if Result.TOO_LOW in results:
                break

    return highest_y_position, results


def in_target_area(position: tuple[int, int], target_area: Area) -> bool:
    x_boundaries, y_boundaries = target_area
    min_x, max_x = x_boundaries
    min_y, max_y = y_boundaries
    x_position, y_position = position

    if x_position < min_x or x_position > max_x:
        return False
    elif y_position < min_y or y_position > max_y:
        return False

    return True


def target_area_unreachable(
    position: tuple[int, int],
    velocity: tuple[int, int],
    target_area: Area,
) -> list[Result]:
    x_boundaries, y_boundaries = target_area
    min_x, max_x = x_boundaries
    min_y, max_y = y_boundaries
    x_position, y_position = position
    x_velocity, y_velocity = velocity

    results = []
    if x_position < min_x and x_velocity <= 0:
        results.append(Result.TOO_EARLY)
    if y_position < min_y and y_velocity <= 0:
        results.append(Result.TOO_LOW)
    if x_position > max_x and x_velocity >= 0:
        results.append(Result.TOO_FAR)

    return results


target_area = read_target_area("input.txt")
highest_y_position = find_highest_y_position(target_area)
print(highest_y_position)
