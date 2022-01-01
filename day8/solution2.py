from typing import Optional

complex_digits_by_segment_count = {
    5: [2, 3, 5],
    6: [0, 6, 9],
}

easy_digits_by_segment_count = {2: 1, 3: 7, 4: 4, 7: 8}


def read_input_and_output_values(filename: str):
    with open(filename, "r") as input_file:
        for line in input_file:
            input_values, output_values = line.split("|")
            input_values = [
                "".join(sorted(value)) for value in input_values.strip().split(" ")
            ]
            output_values = [
                "".join(sorted(value)) for value in output_values.strip().split(" ")
            ]
            yield (input_values, output_values)


def decode_and_sum(filename: str) -> int:
    decoded_sum = 0
    for input_values, output_values in read_input_and_output_values(filename):
        patterns_by_segment_count = map_patterns_to_segment_count(input_values)
        patterns_by_digits = get_patterns_for_digits(patterns_by_segment_count)
        decoded = decode(output_values, patterns_by_digits)
        decoded_sum += decoded

    return decoded_sum


def map_patterns_to_segment_count(patterns: list[str]) -> dict[int, list[str]]:
    patterns_by_segment_count = {}
    for pattern in patterns:
        segment_count = len(pattern)
        patterns_by_segment_count[segment_count] = patterns_by_segment_count.get(
            segment_count, []
        ) + [pattern]

    return patterns_by_segment_count


def patterns_for_easy_digits(
    patterns_by_segment_count: dict[int, list[str]]
) -> list[Optional[str]]:
    patterns_by_digits = [None] * 10
    for segment_count, digit in easy_digits_by_segment_count.items():
        patterns_by_digits[digit] = patterns_by_segment_count.pop(segment_count)[0]

    return patterns_by_digits


def find_3(patterns_by_segment_count: dict[int, list[str]]) -> str:
    patterns = patterns_by_segment_count[5]
    for pattern in patterns:
        difference = 0
        for comparison in patterns:
            difference += len(set(pattern).symmetric_difference(comparison))

        if difference == 4:
            patterns.remove(pattern)
            return pattern


def find_5(
    patterns_by_segment_count: dict[int, list[str]],
    patterns_by_digits: list[Optional[str]],
) -> str:
    return find_number(patterns_by_segment_count[5], patterns_by_digits[4], 3)


def find_9(
    patterns_by_segment_count: dict[int, list[str]],
    patterns_by_digits: list[Optional[str]],
) -> str:
    return find_number(patterns_by_segment_count[6], patterns_by_digits[3], 1)


def find_6(
    patterns_by_segment_count: dict[int, list[str]],
    patterns_by_digits: list[Optional[str]],
) -> str:
    return find_number(patterns_by_segment_count[6], patterns_by_digits[5], 1)


def find_number(
    patterns: list[str],
    comparison_pattern: str,
    identifying_difference: int,
) -> str:
    for pattern in patterns:
        difference = len(set(comparison_pattern).symmetric_difference(pattern))
        if difference == identifying_difference:
            patterns.remove(pattern)
            return pattern


def get_patterns_for_digits(
    patterns_by_segment_count: dict[int, list[str]]
) -> list[str]:
    patterns_by_digits = patterns_for_easy_digits(patterns_by_segment_count)
    patterns_by_digits[3] = find_3(patterns_by_segment_count)
    patterns_by_digits[5] = find_5(patterns_by_segment_count, patterns_by_digits)
    patterns_by_digits[2] = patterns_by_segment_count.pop(5)[0]
    patterns_by_digits[9] = find_9(patterns_by_segment_count, patterns_by_digits)
    patterns_by_digits[6] = find_6(patterns_by_segment_count, patterns_by_digits)
    patterns_by_digits[0] = patterns_by_segment_count.pop(6)[0]
    return patterns_by_digits


def decode(patterns: list[str], patterns_for_digits: list[str]) -> int:
    decoded = ""
    for pattern in patterns:
        decoded += str(patterns_for_digits.index(pattern))

    return int(decoded)


print(decode_and_sum("input.txt"))
