from multiprocessing import Pool


def chunks(lst: list, n: int) -> list:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def progress_timers(timers: list[int], days: int) -> int:
    new_timers = timers
    for day in range(0, days):
        new_timers = calculate_new_timers_for_day(new_timers)

    return len(new_timers)


def calculate_new_timers_for_day(timers: list[int]) -> list[int]:
    new_timers = []
    for timer in timers:
        new_timers.extend(progress_timer(timer))
    return new_timers


def progress_timer(timer: int) -> tuple[int]:
    if timer == 0:
        return (6, 8)
    else:
        return (timer - 1,)


def read_timers(filename: str) -> list[int]:
    with open(filename, "r") as input_file:
        line = input_file.readline()
        return [int(timer) for timer in line.strip().split(",")]


def calculate_lanternfish_amount(timers: list[int], days: int, chunk_count: int) -> int:
    timer_sublists = list(chunks(timers, chunk_count))
    with Pool(processes=chunk_count) as pool:
        results = []
        for sublist in timer_sublists:
            results.append(pool.apply_async(progress_timers, (sublist, days)))
        return sum(res.get() for res in results)


if __name__ == "__main__":
    timers = read_timers("input.txt")
    print(calculate_lanternfish_amount(timers, 80, 10))
