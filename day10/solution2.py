from statistics import median

opening_closing_character_pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
scores = {")": 1, "]": 2, "}": 3, ">": 4}


def compute_autocomplete_score(filename: str) -> int:
    scores = []
    for characters in read_uncorrupted_lines(filename):
        missing_characters = get_missing_characters(characters)
        if not missing_characters:
            continue

        score = compute_score_for_missing_characters(missing_characters)
        scores.append(score)

    return median(sorted(scores))


def read_uncorrupted_lines(filename: str) -> list[str]:
    for characters in read_characters(filename):
        remaining_characters = characters[1:]
        error = has_syntax_error(characters[0], remaining_characters)
        if not error:
            yield characters


def has_syntax_error(character: str, remaining_characters: list[str]) -> bool:
    while True:
        try:
            next_character = remaining_characters.pop(0)
        except IndexError:
            return False

        if next_character in opening_closing_character_pairs:
            error = has_syntax_error(next_character, remaining_characters)
            if error:
                return error
        else:
            break

    expected_character = opening_closing_character_pairs[character]
    return next_character != expected_character


def read_characters(filename: str) -> list[str]:
    with open(filename, "r") as input_file:
        for i, line in enumerate(input_file.readlines()):
            yield list(line.strip())


def get_missing_characters(characters: list[str]) -> list[str]:
    missing_characters = []
    for character in characters:
        try:
            closing_character = opening_closing_character_pairs[character]
            missing_characters.insert(0, closing_character)
        except KeyError:
            missing_characters.remove(character)
    return missing_characters


def compute_score_for_missing_characters(missing_characters: list[str]) -> int:
    score = 0
    for character in missing_characters:
        score *= 5
        score += scores[character]
    return score


print(compute_autocomplete_score("input.txt"))
