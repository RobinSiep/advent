import ast
import copy
import math
from enum import Enum, auto
from typing import Optional, Union


class Action(Enum):
    EXPLODE = auto()
    SPLIT = auto()


def read_numbers(filename: str) -> list:
    numbers = []
    with open(filename) as input_file:
        for line in input_file:
            numbers.append(ast.literal_eval(line.strip()))

    return numbers


def perform_additions(numbers: list) -> list:
    previous_number = None
    for number in numbers:
        if not previous_number:
            previous_number = number
            continue

        previous_number = add(previous_number, number)

    return previous_number


def add(number_1: list, number_2: list) -> list:
    return reduce([number_1, number_2])


def reduce(number: list) -> list:
    indexes, action_type = find_next_action(number)
    if not action_type:
        return number

    if action_type == Action.EXPLODE:
        new_number = explode(number, indexes)
    elif action_type == Action.SPLIT:
        new_number = split(number, indexes)

    return reduce(new_number)


def find_next_action(
    number: list, indexes: Optional[list[int]] = None
) -> tuple[list[int], Action]:
    found_action_type = None
    found_indexes = None
    if not indexes:
        indexes = []

    if isinstance(number, list):
        if len(indexes) == 4:
            return indexes, Action.EXPLODE

        for i, sub_number in enumerate(number):
            new_indexes, action_type = find_next_action(sub_number, indexes + [i])
            if action_type == Action.EXPLODE:
                return new_indexes, action_type
            elif action_type and not found_action_type:
                found_action_type = action_type
                found_indexes = new_indexes
    elif isinstance(number, int) and number >= 10:
        return indexes, Action.SPLIT

    return found_indexes, found_action_type


def explode(number: list, indexes: list[int]) -> list:
    new_number = copy.copy(number)
    exploding_pair = get(new_number, indexes)
    left_indexes = get_left_explosion_indexes(indexes, new_number)
    right_indexes = get_right_explosion_indexes(indexes, new_number)

    if left_indexes:
        add_regular_number(new_number, left_indexes, exploding_pair[0])
    if right_indexes:
        add_regular_number(new_number, right_indexes, exploding_pair[1])

    replace(new_number, indexes, 0)
    return new_number


def get(number: list, indexes: list[int]) -> list:
    indexes = copy.copy(indexes)
    if not indexes:
        return number
    return get(number[indexes.pop(0)], indexes)


def replace(number: list, indexes: list[int], replacement: Union[list, int]) -> None:
    indexes = copy.copy(indexes)
    if len(indexes) == 1:
        number[indexes[0]] = replacement
        return

    replace(number[indexes.pop(0)], indexes, replacement)


def add_regular_number(number: list, indexes: list[int], regular_number: int) -> None:
    indexes = copy.copy(indexes)
    if len(indexes) == 1:
        number[indexes[0]] += regular_number
        return

    add_regular_number(number[indexes.pop(0)], indexes, regular_number)


def get_left_explosion_indexes(indexes: list[int], number: list) -> list[int]:
    left_indexes = copy.copy(indexes)
    while left_indexes:
        left_index = left_indexes.pop() - 1
        new_left_indexes = left_indexes + [left_index]
        if left_index >= 0:
            return get_indexes_for_rightmost_regular_number(number, new_left_indexes)

    return []


def get_right_explosion_indexes(indexes: list[int], number: list) -> list[int]:
    right_indexes = copy.copy(indexes)
    while right_indexes:
        right_index = right_indexes.pop() + 1
        new_right_indexes = right_indexes + [right_index]
        try:
            get(number, new_right_indexes)
            return get_indexes_for_leftmost_regular_number(number, new_right_indexes)
        except (IndexError, TypeError):
            pass

    return []


def get_indexes_for_leftmost_regular_number(
    number: list, indexes: list[int]
) -> list[int]:
    number_for_indexes = get(number, indexes)
    if isinstance(number_for_indexes, int):
        return indexes

    return get_indexes_for_leftmost_regular_number(number, indexes + [0])


def get_indexes_for_rightmost_regular_number(
    number: list, indexes: list[int]
) -> list[int]:
    number_for_indexes = get(number, indexes)
    if isinstance(number_for_indexes, int):
        return indexes

    return get_indexes_for_rightmost_regular_number(
        number, indexes + [len(number_for_indexes) - 1]
    )


def split(number: list, indexes: list[int]) -> list:
    new_number = copy.copy(number)
    number_to_split = get(new_number, indexes)
    divided = number_to_split / 2
    replace(new_number, indexes, [math.floor(divided), math.ceil(divided)])
    return new_number


def calculate_magnitude(number: list) -> int:
    if isinstance(number, int):
        return number

    left, right = number
    if isinstance(left, list):
        left = calculate_magnitude(left)
    if isinstance(right, list):
        right = calculate_magnitude(right)

    return left * 3 + right * 2


numbers = read_numbers("input.txt")
result = perform_additions(numbers)
print(calculate_magnitude(result))
