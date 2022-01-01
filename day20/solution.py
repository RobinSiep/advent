import copy

PADDING = 3
DEBUG = False
Image = list[list[int]]


def read_image_and_enhancement_algo(filename: str) -> tuple[Image, list[int]]:
    enhancement_algo = []
    image = []

    with open(filename, "r") as input_file:
        lines = input_file.readlines()

    enhancement_algo = parse_to_binary_list(lines.pop(0))
    lines.pop(0)
    for line in lines:
        image.append(parse_to_binary_list(line))

    return image, enhancement_algo


def parse_to_binary_list(line: str) -> list[int]:
    binary_list = []
    for pixel in line.strip():
        binary_pixel = 1 if pixel == "#" else 0
        binary_list.append(binary_pixel)

    return binary_list


def wrap(image: Image, filler: int = 0) -> Image:
    debug_print("")
    debug_print("input")
    debug_print(image)
    debug_print("")
    new_image = copy.deepcopy(image)
    line_length = len(new_image[0])
    filler_line = [filler] * line_length
    for _ in range(PADDING):
        new_image.insert(0, copy.copy(filler_line))
        new_image.append(copy.copy(filler_line))

    for line in new_image:
        for _ in range(PADDING):
            line.insert(0, filler)
            line.append(filler)

    debug_print("output")
    debug_print(new_image)
    return new_image


def calculate_lit_pixels(image: Image) -> int:
    return sum((sum(row) for row in image))


def apply_image_enhancements(
    image: Image,
    enhancement_algo: list[int],
    number_of_times: int,
) -> Image:
    new_image = copy.deepcopy(image)
    for _ in range(number_of_times):
        enhanced = enhance(new_image, enhancement_algo)
        new_image = wrap(enhanced, enhanced[0][0])

    return new_image


def enhance(image: Image, enhancement_algo: list[int]) -> Image:
    new_image = []
    for row_index, row in enumerate(image):
        new_row = []
        for column_index, pixel in enumerate(row):
            try:
                enhancement_index = get_enhancement_index(
                    image, row_index, column_index
                )
            except ValueError:
                # Dirty flip of infinite remaining pixels
                new_row.append(int(not bool(image[0][0])))
                continue

            new_row.append(enhancement_algo[enhancement_index])

        new_image.append(new_row)

    return new_image


def get_enhancement_index(image: Image, x: int, y: int) -> int:
    binary_index = []
    lookup_indexes = get_lookup_indexes(x, y)
    if contains_negative_index(lookup_indexes):
        raise ValueError

    try:
        for lookup_x, lookup_y in lookup_indexes:
            binary_index.append(image[lookup_x][lookup_y])
    except IndexError:
        raise ValueError

    return int("".join([str(i) for i in binary_index]), 2)


def get_lookup_indexes(x: int, y: int) -> tuple[int, ...]:
    return (
        (x - 1, y - 1),
        (x - 1, y),
        (x - 1, y + 1),
        (x, y - 1),
        (x, y),
        (x, y + 1),
        (x + 1, y - 1),
        (x + 1, y),
        (x + 1, y + 1),
    )


def contains_negative_index(lookup_indexes: tuple[int, ...]) -> bool:
    for indexes in lookup_indexes:
        for index in indexes:
            if index < 0:
                return True

    return False


def debug_print(value: any) -> None:
    if not DEBUG:
        return

    if isinstance(value, str) or isinstance(value, int):
        return print(value)

    for line in value:
        print("".join([str(x) for x in line]))


image, enhancement_algo = read_image_and_enhancement_algo("input.txt")
wrapped_image = wrap(image)
debug_print(wrapped_image)
enhanced_image = apply_image_enhancements(wrapped_image, enhancement_algo, 2)
lit_pixels = calculate_lit_pixels(enhanced_image)
print(lit_pixels)
