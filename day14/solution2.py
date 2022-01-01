def read(filename: str) -> tuple[dict[str, int], dict[str, str]]:
    # Elements by count
    insertion_rules = {}
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        polymer_template = parse_polymer_template(lines.pop(0).strip())

        # Pop divider line
        lines.pop(0)
        for line in lines:
            key, element = line.split("->")
            insertion_rules[key.strip()] = element.strip()

    return polymer_template, insertion_rules


def parse_polymer_template(line: str) -> dict[str, int]:
    polymer_template = {}
    for i in range(len(line)):
        try:
            pair = line[i] + line[i + 1]
        except IndexError:
            break

        polymer_template[pair] = polymer_template.get(pair, 0) + 1
    return polymer_template


def execute_insertions(
    polymer_template: dict[str, int],
    insertion_rules: dict[str, str],
    steps: int,
) -> dict[str, int]:
    polymer = polymer_template
    for _ in range(steps):
        polymer = insert(polymer, insertion_rules)

    return polymer


def insert(polymer: dict[str, int], insertion_rules: dict[str, str]) -> dict[str, int]:
    new_polymer = {}
    for pair, element in insertion_rules.items():
        try:
            existing_count = polymer.pop(pair)
        except KeyError:
            continue

        new_pair_1 = pair[0] + element
        new_pair_2 = element + pair[1]
        new_polymer[new_pair_1] = new_polymer.get(new_pair_1, 0) + existing_count
        new_polymer[new_pair_2] = new_polymer.get(new_pair_2, 0) + existing_count

    return new_polymer


def calculate_element_quantity_difference(polymer: dict[str, int]) -> int:
    element_quantities = {}
    for pair, count in polymer.items():
        for i, element in enumerate(pair):
            current_count = element_quantities.get(element, (0, 0))
            new_count = list(current_count)
            new_count[i] += count
            element_quantities[element] = tuple(new_count)

    quantities = [max(counts) for counts in element_quantities.values()]
    return max(quantities) - min(quantities)


polymer_template, insertion_rules = read("input.txt")
polymer = execute_insertions(polymer_template, insertion_rules, 40)
element_quantity_difference = calculate_element_quantity_difference(polymer)
print(element_quantity_difference)
