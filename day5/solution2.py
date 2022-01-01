class Diagram:
    points = {}

    def add_line(self, start: tuple[str, str], end: tuple[str, str]):
        start_x, start_y = start
        end_x, end_y = end
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        step = 1

        if start_x == end_x:
            if start_y > end_y:
                step = -1

            for y in range(int(start_y), end_y + step, step):
                self._add_point(start_x, y)
        elif start_y == end_y:
            if start_x > end_x:
                step = -1

            for x in range(start_x, end_x + step, step):
                self._add_point(x, start_y)
        else:
            y_step = 1
            if start_x > end_x:
                step = -1
            if start_y > end_y:
                y_step = -1

            y = start_y
            for x in range(start_x, end_x + step, step):
                self._add_point(x, y)
                y += y_step

    def _add_point(self, x: int, y: int) -> None:
        self.points[(x, y)] = self.points.get((x, y), 0) + 1

    def count_dangerous_points(self) -> int:
        dangerous_points = 0
        for point, line_count in self.points.items():
            if line_count >= 2:
                dangerous_points += 1

        return dangerous_points


def read_diagram(filename: str) -> Diagram:
    diagram = Diagram()
    with open(filename, "r") as input_file:
        for line in input_file:
            line = line.strip()
            start, end = [points.strip() for points in line.split("->")]
            diagram.add_line(start.split(","), end.split(","))

    return diagram


diagram = read_diagram("input.txt")
print(diagram.count_dangerous_points())
