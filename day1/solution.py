increases = 0
with open("input.txt", "r") as input_file:
    previous = None
    for line in input_file:
        value = int(line)
        if previous is not None and value > previous:
            increases += 1

        previous = value
print(increases)
