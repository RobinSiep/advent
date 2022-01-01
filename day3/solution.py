class DiagnosticReader:
    zeros: [int] = []
    ones: [int] = []

    def __init__(self, filename: str) -> None:
        self._read(filename)

    def _read(self, filename: str) -> None:
        with open(filename, "r") as input_file:
            for line in input_file:
                for i, bit in enumerate(line.strip()):
                    self._increment_bit(i, bit)

    def _increment_bit(self, index: int, bit: str) -> None:
        try:
            if bit == "0":
                self.zeros[index] = self.zeros[index] + 1
            else:
                self.ones[index] = self.ones[index] + 1
        except IndexError:
            self.zeros.append(0)
            self.ones.append(0)
            self._increment_bit(index, bit)

    def _calculate_rates(self) -> tuple[int, int]:
        gamma_bits = ""
        epsilon_bits = ""
        for i, total_zeros in enumerate(self.zeros):
            total_ones = self.ones[i]
            if total_zeros > total_ones:
                gamma_bits += "0"
                epsilon_bits += "1"
            else:
                gamma_bits += "1"
                epsilon_bits += "0"

        return (int(gamma_bits, 2), int(epsilon_bits, 2))

    def print_power_consumption(self) -> int:
        gamma_rate, epsilon_rate = self._calculate_rates()
        power_consumption = gamma_rate * epsilon_rate
        print(power_consumption)
        return power_consumption


DiagnosticReader("input.txt").print_power_consumption()
