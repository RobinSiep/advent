unique_number_of_segments = [2, 3, 4, 7]


def count_digits_with_unique_segments(filename: str) -> int:
    digits_with_unique_segments = 0
    for output_values in read_output_values(filename):
        output_segments = [len(output) for output in output_values]

        for number_of_segments in unique_number_of_segments:
            digits_with_unique_segments += output_segments.count(number_of_segments)

    return digits_with_unique_segments


def read_output_values(filename: str) -> list[str]:
    with open(filename, "r") as input_file:
        for line in input_file:
            _, output_values = line.strip().split("|")
            yield output_values.split(" ")


print(count_digits_with_unique_segments("input.txt"))
