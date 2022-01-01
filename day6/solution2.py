def calculate_lanternfish_amount(timers: list[int], days: int) -> int:
    new_timers = timers
    for day in range(0, days):
        day_0 = new_timers.pop(0)
        new_timers.append(day_0)
        new_timers[6] += day_0

    return sum(new_timers)


def read_timers_grouped_by_value(filename: str) -> list[int]:
    timers = []
    with open(filename, "r") as input_file:
        line = input_file.readline()
        timers_ = [int(timer) for timer in line.strip().split(",")]
        for i in range(0, 9):
            timers.append(len([timer for timer in timers_ if timer == i]))
    return timers


timers = read_timers_grouped_by_value("input.txt")
print(calculate_lanternfish_amount(timers, 256))
