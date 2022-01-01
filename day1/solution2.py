from typing import Optional


class SlidingWindow:
    increases = 0
    sliding: list[list[int]] = []
    previous_sum: Optional[int] = None

    def add_measurement(self, measurement: int) -> None:
        for existing_window in self.sliding:
            existing_window.append(measurement)
        self.sliding.append([measurement])
        self._pop_completed_window()

    def _pop_completed_window(self):
        if len(self.sliding[0]) == 3:
            complete_window = self.sliding.pop(0)
            sliding_sum = sum(complete_window)
            if self.previous_sum and sliding_sum > self.previous_sum:
                self.increases += 1

            self.previous_sum = sliding_sum


def count_increases(filename: str) -> int:
    sliding_window = SlidingWindow()
    with open("input.txt", "r") as input_file:
        for line in input_file:
            sliding_window.add_measurement(int(line))
    return sliding_window.increases


print(count_increases("input.txt"))
