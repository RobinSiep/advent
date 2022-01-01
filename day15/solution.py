from queue import PriorityQueue


class Risk:
    id_: int
    weight: int

    def __init__(self, id_: int, weight: int) -> None:
        self.id_ = id_
        self.weight = weight


class Graph:
    number_of_vertices: int

    def __init__(self, num_of_vertices: int) -> None:
        self.number_of_vertices = num_of_vertices
        self.edges = [
            [-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)
        ]
        self.visited = []

    def add_edge(self, risk_1: Risk, risk_2: Risk) -> None:
        self.edges[risk_1.id_][risk_2.id_] = risk_2.weight
        self.edges[risk_2.id_][risk_1.id_] = risk_1.weight


def run_dijkstra(graph, start_vertex) -> dict[int, int]:
    dijkstra: dict[int, int] = {
        v: float("inf") for v in range(graph.number_of_vertices)
    }
    dijkstra[start_vertex] = 0

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.number_of_vertices):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = dijkstra[neighbor]
                    new_cost = dijkstra[current_vertex] + distance
                    if new_cost < old_cost:
                        pq.put((new_cost, neighbor))
                        dijkstra[neighbor] = new_cost
    return dijkstra


def read(filename: str) -> Graph:
    with open(filename, "r") as input_file:
        lines = input_file.readlines()

        risk_map, size = read_risk_map(lines)
        risk_graph = read_risk_graph(risk_map, size)

    return risk_graph


def read_risk_map(lines: list[str]) -> tuple[list[Risk], int]:
    risk_map = []

    id_counter = 0
    for line in lines:
        row = []
        for risk in list(line.strip()):
            row.append(Risk(id_counter, int(risk)))
            id_counter += 1
        risk_map.append(row)

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
dijkstra = run_dijkstra(risk_graph, 0)
print(dijkstra[risk_graph.number_of_vertices - 1])
