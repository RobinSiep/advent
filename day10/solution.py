opening_closing_character_pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
scores = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def read_characters(filename: str) -> list[str]:
    with open(filename, "r") as input_file:
        for i, line in enumerate(input_file.readlines()):
            yield list(line.strip())


def compute_syntax_error_score_sum(filename: str) -> int:
    syntax_error_score = 0
    for characters in read_characters(filename):
        remaining_characters = characters[1:]
        error = find_syntax_error_score(characters[0], remaining_characters)
        syntax_error_score += error

    return syntax_error_score


def find_syntax_error_score(character: str, remaining_characters: list[str]) -> int:
    while True:
        try:
            next_character = remaining_characters.pop(0)
        except IndexError:
            return 0

        if next_character in opening_closing_character_pairs:
            error_score = find_syntax_error_score(next_character, remaining_characters)
            if error_score:
                return error_score
        else:
            break

    expected_character = opening_closing_character_pairs[character]
    if next_character == expected_character:
        return 0
    else:
        return scores[next_character]


syntax_error_score = compute_syntax_error_score_sum("input.txt")
print(syntax_error_score)
