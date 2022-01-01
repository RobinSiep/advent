from __future__ import annotations

import copy
from typing import Optional

Coordinates = tuple[int, int, int]
Distance = tuple[int, int, int]


class Beacon:
    coordinates: Coordinates

    def __init__(self, coordinates: Coordinates) -> None:
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.z = coordinates[2]

    def __repr__(self) -> str:
        return str(self.coordinates)

    def __hash__(self) -> int:
        return hash(self.coordinates)

    def __eq__(self, other: any) -> bool:
        return hash(self) == hash(other)

    def rotated_along_x(self) -> Beacon:
        return Beacon((self.x, self.z * -1, self.y))

    def rotated_along_y(self) -> Beacon:
        return Beacon((self.z * -1, self.y, self.x))

    def rotated_along_z(self) -> Beacon:
        return Beacon((self.y, self.x * -1, self.z))

    def moved(self, distance: Distance) -> Beacon:
        return Beacon(
            (self.x + distance[0], self.y + distance[1], self.z + distance[2])
        )

    def calculate_distance(self, other) -> Distance:
        return (other.x - self.x, other.y - self.y, other.z - self.z)


class Scanner:
    location: Coordinates
    beacons: frozenset[Beacon]
    normalized_cache: dict[tuple[Scanner, Scanner], Optional[Scanner]] = {}

    def __init__(
        self,
        beacons: frozenset[Beacon],
        location: Coordinates = (0, 0, 0),
    ) -> None:
        self.beacons = beacons
        self.location = location

    def generate_rotations(self) -> set[Scanner]:
        rotations = set()
        rotated = self
        for x in range(4):
            rotated = rotated.rotated_along_x()
            for y in range(4):
                rotated = rotated.rotated_along_y()
                for z in range(4):
                    rotated = rotated.rotated_along_z()
                    rotations.add(rotated)
        return rotations

    def rotated_along_x(self) -> Scanner:
        rotated_beacons = frozenset(beacon.rotated_along_x() for beacon in self.beacons)
        return Scanner(rotated_beacons)

    def rotated_along_y(self) -> Scanner:
        rotated_beacons = frozenset(beacon.rotated_along_y() for beacon in self.beacons)
        return Scanner(rotated_beacons)

    def rotated_along_z(self) -> Scanner:
        rotated_beacons = frozenset(beacon.rotated_along_z() for beacon in self.beacons)
        return Scanner(rotated_beacons)

    def __repr__(self) -> str:
        beacons_str = ""
        for beacon in self.beacons:
            beacons_str += str(beacon) + "\n"
        return beacons_str + "\n"

    def __hash__(self) -> int:
        return hash(self.beacons)

    def __eq__(self, other: any) -> int:
        return hash(self) == hash(other)

    def normalized(
        self,
        reference: Scanner,
        overlap_threshold: int,
    ) -> Optional[Scanner]:
        distances = {}
        cache_key = (self, reference)
        cache = type(self).normalized_cache
        try:
            return cache[cache_key]
        except KeyError:
            pass

        for beacon in self.beacons:
            for reference_beacon in reference.beacons:
                distance = beacon.calculate_distance(reference_beacon)
                count = distances.get(distance, 0) + 1
                if count == overlap_threshold:
                    normalized = Scanner(
                        frozenset(beacon.moved(distance) for beacon in self.beacons),
                        (
                            self.location[0] + distance[0],
                            self.location[1] + distance[1],
                            self.location[2] + distance[2],
                        ),
                    )
                    cache[cache_key] = normalized
                    return normalized

                distances[distance] = count
        cache[cache_key] = None

    def calculate_manhattan_distance(self, other: Scanner) -> int:
        return sum(
            (
                abs(self.location[0] - other.location[0]),
                abs(self.location[1] - other.location[1]),
                abs(self.location[2] - other.location[2]),
            )
        )


def read_scanners(filename: str) -> list[Scanner]:
    scanners = []
    beacons = set()
    with open(filename) as input_file:
        for line in input_file:
            stripped = line.strip()
            if not stripped:
                scanners.append(Scanner(frozenset(beacons)))
                beacons = set()
                continue
            elif "---" in stripped:
                continue

            beacons.add(
                Beacon(tuple(int(coordinate) for coordinate in stripped.split(",")))
            )

    scanners.append(Scanner(frozenset(beacons)))
    return scanners


def generate_rotations(scanners: list[Scanner]) -> dict[Scanner, frozenset[Scanner]]:
    rotations = {}
    for scanner in scanners:
        rotations[scanner] = scanner.generate_rotations()
    return rotations


def normalize(
    scanners: list[Scanner],
    overlap_threshold: int,
    origin_index: int = 0,
) -> list[Scanner]:
    scanners = copy.copy(scanners)
    normalized = [scanners.pop(origin_index)]
    while scanners:
        for i, scanner in enumerate(scanners):
            new_normalized_scanner = normalize_scanner(
                normalized, scanner, overlap_threshold
            )
            if new_normalized_scanner:
                normalized.append(new_normalized_scanner)
                del scanners[i]

    return normalized


def normalize_scanner(
    previously_normalized: list[Scanner],
    target: Scanner,
    overlap_threshold: int,
) -> Optional[Scanner]:
    for rotated in rotations[target]:
        for normalized_scanner in previously_normalized:
            new_normalized_scanner = rotated.normalized(
                normalized_scanner, overlap_threshold
            )
            if new_normalized_scanner:
                return new_normalized_scanner


def calculate_largest_manhattan_distance(scanners: list[Scanner]) -> int:
    distance = 0
    for scanner in scanners:
        for other in scanners:
            if scanner is other:
                continue

            distance = max(distance, scanner.calculate_manhattan_distance(other))

    return distance


scanners = read_scanners("input.txt")
rotations = generate_rotations(scanners)
normalized_scanners = normalize(scanners, 12)
print(calculate_largest_manhattan_distance(normalized_scanners))
