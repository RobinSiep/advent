from typing import Type

hexadecimal_to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class Packet:
    version: int
    type_id: int

    def __init__(self, version: int, type_id: int) -> None:
        self.version = version
        self.type_id = type_id

    def get_summed_versions(self) -> int:
        return self.version


class LiteralValuePacket(Packet):
    value_binary_repr: str

    def __init__(self, version: int, type_id: int, value_binary_repr: str) -> None:
        super().__init__(version, type_id)
        self.value_binary_repr = value_binary_repr

    @property
    def value(self) -> int:
        return int(self.value_binary_repr, 2)


class OperatorPacket(Packet):
    sub_packets: [Packet]
    operator: "Operator"

    def __init__(self, version: int, type_id: int, sub_packets: [Packet]) -> None:
        super().__init__(version, type_id)
        self.sub_packets = sub_packets
        self.operator = self.get_operator_for_type_id(type_id, sub_packets)

    def get_summed_versions(self) -> int:
        sub_sum = sum([packet.get_summed_versions() for packet in self.sub_packets])
        return super().get_summed_versions() + sub_sum

    @property
    def value(self) -> int:
        return self.operator()

    @staticmethod
    def get_operator_for_type_id(
        type_id: int, sub_packets: list[Packet]
    ) -> Type["Operator"]:
        return type_id_to_operator_class[type_id](sub_packets)


class Operator:
    values: [int]

    def __init__(self, sub_packets: list[Packet]) -> None:
        self.values = [packet.value for packet in sub_packets]

    def __call__(self) -> int:
        raise NotImplementedError


class SumOperator(Operator):
    def __call__(self) -> int:
        return sum(self.values)


class ProductOperator(Operator):
    def __call__(self) -> int:
        product = 1
        for value in self.values:
            product *= value
        return product


class MinimumOperator(Operator):
    def __call__(self) -> int:
        return min(self.values)


class MaximumOperator(Operator):
    def __call__(self) -> int:
        return max(self.values)


class GreaterThanOperator(Operator):
    def __call__(self) -> int:
        return int(self.values[0] > self.values[1])


class LessThanOperator(Operator):
    def __call__(self) -> int:
        return int(self.values[0] < self.values[1])


class EqualOperator(Operator):
    def __call__(self) -> int:
        return int(self.values[0] == self.values[1])


type_id_to_operator_class = {
    0: SumOperator,
    1: ProductOperator,
    2: MinimumOperator,
    3: MaximumOperator,
    5: GreaterThanOperator,
    6: LessThanOperator,
    7: EqualOperator,
}


def read_as_binary_string(filename: str) -> str:
    with open(filename, "r") as input_file:
        line = input_file.readlines()[0].strip()
    return "".join([hexadecimal_to_binary[char] for char in line])


def decode_until_complete(binary_list: list[str]) -> list[Packet]:
    packets = []
    while "1" in binary_list:
        packets.append(decode(binary_list))
    return packets


def decode(binary_list: list[str]) -> Packet:
    type_id_bits = binary_list[3:6]

    type_id = int("".join(type_id_bits), 2)
    if type_id == 4:
        return decode_literal_value_packet(binary_list)
    else:
        return decode_operator_packet(binary_list)


def pop_version_and_type_id(binary_list: list[str]) -> tuple[int, int]:
    version = int("".join(binary_list[0:3]), 2)
    del binary_list[0:3]
    type_id = int("".join(binary_list[0:3]), 2)
    del binary_list[0:3]
    return version, type_id


def decode_literal_value_packet(binary_list: list[str]) -> LiteralValuePacket:
    version, type_id = pop_version_and_type_id(binary_list)
    value = []
    while True:
        group = binary_list[0:5]
        del binary_list[0:5]
        final_group = not bool(int(group[0]))
        value += group[1:5]
        if final_group:
            break

    return LiteralValuePacket(version, type_id, "".join(value))


def decode_operator_packet(binary_list: list[str]) -> OperatorPacket:
    version, type_id = pop_version_and_type_id(binary_list)
    length_type_id = binary_list[0]
    del binary_list[0]
    if length_type_id == "0":
        return decode_operator_packet_by_sub_packet_length(
            version, type_id, binary_list
        )
    else:
        return decode_operator_packet_by_sub_packet_count(version, type_id, binary_list)


def decode_operator_packet_by_sub_packet_length(
    version: int, type_id: int, binary_list: list[str]
) -> OperatorPacket:
    sub_packet_length = int("".join(binary_list[:15]), 2)
    del binary_list[:15]
    sub_packets_string = binary_list[:sub_packet_length]
    del binary_list[:sub_packet_length]
    sub_packets = []
    while sub_packets_string:
        sub_packets.append(decode(sub_packets_string))

    return OperatorPacket(version, type_id, sub_packets)


def decode_operator_packet_by_sub_packet_count(
    version: int, type_id: int, binary_list: list[str]
) -> OperatorPacket:
    sub_packet_count = int("".join(binary_list[:11]), 2)
    del binary_list[:11]
    sub_packets = []
    for i in range(sub_packet_count):
        sub_packets.append(decode(binary_list))

    return OperatorPacket(version, type_id, sub_packets)


binary_string = read_as_binary_string("input.txt")
packet = decode(list(binary_string))
print(packet.value)
