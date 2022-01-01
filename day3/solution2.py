lines = []
possible_oxygen_data = []
possible_co2_data = []
most_common_bits = ""


def calculate_zero_and_one_distribution(data):
    zeros = []
    ones = []
    for line in data:
        for i, bit in enumerate(line):
            increment_bit(i, bit, zeros, ones)

    return (zeros, ones)


def increment_bit(index, bit, zeros, ones):
    try:
        if bit == "0":
            zeros[index] = zeros[index] + 1
        else:
            ones[index] = ones[index] + 1
    except IndexError:
        zeros.append(0)
        ones.append(0)
        increment_bit(index, bit, zeros, ones)


def filter_data_for_bit(data, bit, index):
    if len(data) == 1:
        return data

    return [line for line in data if line[index] == bit]


def find_data_for_bit_criteria(data, most_common, index=0):
    if len(data) == 1:
        return data[0]

    zeros, ones = calculate_zero_and_one_distribution(data)
    total_zeros = zeros[index]
    total_ones = ones[index]

    if total_zeros > total_ones:
        criteria = "0" if most_common else "1"
        data = filter_data_for_bit(data, criteria, index)
    else:
        criteria = "1" if most_common else "0"
        data = filter_data_for_bit(data, criteria, index)

    return find_data_for_bit_criteria(data, most_common, index + 1)


with open("input.txt", "r") as input_file:
    for line in input_file:
        line = line.strip()
        possible_oxygen_data.append(line)
        possible_co2_data.append(line)


oxygen_bits = find_data_for_bit_criteria(possible_oxygen_data, True)
co2_bits = find_data_for_bit_criteria(possible_co2_data, False)
oxygen = int(oxygen_bits, 2)
co2 = int(co2_bits, 2)
life_support = oxygen * co2
print(life_support)
