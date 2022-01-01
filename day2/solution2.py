horizontal = 0
depth = 0
aim = 0
with open("input.txt", "r") as input_file:
    for line in input_file:
        instruction, value = line.split(" ")
        value = int(value)
        if instruction == "forward":
            horizontal += value
            depth += aim * value
        elif instruction == "down":
            aim += value
        elif instruction == "up":
            aim -= value

print(horizontal * depth)
