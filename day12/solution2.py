class Cave:
    value: str
    large: bool

    def __init__(self, value: str) -> None:
        self.value = value
        self.large = value.isupper()

    def __repr__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __eq__(self, other: any) -> bool:
        return self.value == other.value


def read(filename: str) -> dict[Cave, set[Cave]]:
    connections = {}
    with open(filename, "r") as input_file:
        for line in input_file:
            point1, point2 = line.strip().split("-")
            cave1 = Cave(point1)
            cave2 = Cave(point2)
            connections[cave1] = set.union(connections.get(cave1, set()), {cave2})
            connections[cave2] = set.union(connections.get(cave2, set()), {cave1})
    return connections


def find_paths(
    connections: dict[Cave, set[Cave]],
    current_path: tuple[Cave],
) -> list[tuple[Cave]]:
    completed_paths = []
    from_ = current_path[-1]

    for connecting_cave in connections[from_]:
        new_path = current_path + (connecting_cave,)
        if connecting_cave.value == "end":
            completed_paths.append(new_path)
            continue
        elif connecting_cave.value == "start":
            continue
        elif (
            not connecting_cave.large
            and connecting_cave in current_path
            and not may_revisit_small_cave(current_path)
        ):
            continue

        completed_paths += find_paths(connections, new_path)

    return completed_paths


def may_revisit_small_cave(current_path: tuple[Cave]) -> bool:
    small_caves_visited = [cave for cave in current_path if not cave.large]
    return len(set(small_caves_visited)) == len(small_caves_visited)


connections = read("input.txt")
paths = find_paths(connections, (Cave("start"),))
print(len(paths))
