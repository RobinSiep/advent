import math
from collections import defaultdict
from heapq import heappop, heappush
from typing import Optional


class Risk:
    id_: int
    weight: int

    def __init__(self, id_: int, weight: int) -> None:
        self.id_ = id_
        self.weight = weight


class Graph:
    edges: list[tuple[int, int, int]] = []
    size: int

    def __init__(self, size: int) -> None:
        self.size = size

    def add_edge(self, risk_1: Risk, risk_2: Risk) -> None:
        self.edges.append((risk_1.id_, risk_2.id_, risk_2.weight))
        self.edges.append((risk_2.id_, risk_1.id_, risk_1.weight))


def dijkstra(
    edges: list[tuple[int, int, int]],
    start: int,
    target: int,
) -> tuple[float | int, Optional[tuple]]:
    graph = defaultdict(list)
    for left, right, weight in edges:
        graph[left].append((weight, right))

    queue, seen, mins = [(0, start, ())], set(), {start: 0}
    while queue:
        (weight_1, vertex_1, path) = heappop(queue)
        if vertex_1 not in seen:
            seen.add(vertex_1)
            path = (vertex_1, path)
            if vertex_1 == target:
                return (weight_1, path)

            for weight_2, vertex_2 in graph.get(vertex_1, ()):
                if vertex_2 in seen:
                    continue

                prev = mins.get(vertex_2, None)
                next_ = weight_1 + weight_2
                if prev is None or next_ < prev:
                    mins[vertex_2] = next_
                    heappush(queue, (next_, vertex_2, path))

    return float("inf"), None


def read(filename: str) -> Graph:
    with open(filename, "r") as input_file:
        lines = input_file.readlines()

        risk_map, size = read_risk_map(lines)
        risk_graph = read_risk_graph(risk_map, size)

    return risk_graph


def read_risk_map(lines: list[str]) -> tuple[list[Risk], int]:
    modifier = 5
    risk_map = []

    id_counter = 0
    x_length = len(lines)
    for x in range(x_length * modifier):
        x_scale = math.floor(x / x_length)
        new_row = []
        line = lines[x % x_length]
        row = list(line.strip())
        y_length = len(row)
        for y in range(y_length * modifier):
            y_scale = math.floor(y / y_length)
            number_of_repeats = max(0, x_scale + y_scale)
            original_risk_value = int(line[y % y_length])
            scaled_risk_value = original_risk_value + number_of_repeats
            if scaled_risk_value > 9:
                scaled_risk_value %= 9
            risk = Risk(id_counter, scaled_risk_value)
            new_row.append(risk)
            id_counter += 1

        risk_map.append(new_row)

    return risk_map, id_counter


def read_risk_graph(risk_map: list[Risk], size: int) -> Graph:
    risk_graph = Graph(size)
    for x, row in enumerate(risk_map):
        for y, risk in enumerate(row):
            try:
                risk_graph.add_edge(risk, row[y + 1])
            except IndexError:
                pass

            try:
                risk_graph.add_edge(risk, risk_map[x + 1][y])
            except IndexError:
                pass

    return risk_graph


risk_graph = read("input.txt")
D = dijkstra(risk_graph.edges, 0, risk_graph.size - 1)
print(D[0])
