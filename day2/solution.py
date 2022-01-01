horizontal = 0
depth = 0
with open("input.txt", "r") as input_file:
    for line in input_file:
        instruction, value = line.split(" ")
        value = int(value)
        if instruction == "forward":
            horizontal += value
        elif instruction == "down":
            depth += value
        elif instruction == "up":
            depth -= value

print(horizontal * depth)
