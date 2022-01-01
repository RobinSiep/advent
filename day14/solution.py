from collections import Counter


def read(filename: str) -> tuple[str, dict[str, str]]:
    polymer_template = ""
    insertion_rules = {}
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        polymer_template = lines.pop(0).strip()
        # Pop divider line
        lines.pop(0)
        for line in lines:
            key, element = line.split("->")
            insertion_rules[key.strip()] = element.strip()

    return polymer_template, insertion_rules


def execute_insertions(
    polymer_template: str,
    insertion_rules: dict[str, str],
    steps: int,
) -> str:
    polymer = polymer_template
    for _ in range(steps):
        polymer = insert(polymer, insertion_rules)

    return polymer


def insert(polymer: str, insertion_rules: dict[str, str]) -> str:
    new_polymer = list(polymer)
    i = 0
    while True:
        try:
            pair = new_polymer[i] + new_polymer[i + 1]
            new_element = insertion_rules[pair]
        except KeyError:
            i += 1
            continue
        except IndexError:
            break

        new_polymer.insert(i + 1, new_element)
        i += 2

    return "".join(new_polymer)


def calculate_extreme_quantity_difference(polymer: str) -> int:
    counter = Counter(polymer)
    counts = counter.most_common()
    return counts[0][1] - counts[-1][1]


polymer_template, insertion_rules = read("input.txt")
polymer = execute_insertions(polymer_template, insertion_rules, 10)
extreme_quantity_difference = calculate_extreme_quantity_difference(polymer)
print(extreme_quantity_difference)
