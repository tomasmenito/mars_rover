from enum import Enum


class CardinalDirection(Enum):
    def __init__(self, sign: str, vector: tuple[int, int]):
        self.sign = sign
        self.vector = vector

    NORTH = ("N", (0, 1))
    EAST = ("E", (1, 0))
    SOUTH = ("S", (0, -1))
    WEST = ("W", (-1, 0))

    @property
    def clockwise_next(self):
        options = list(CardinalDirection)
        index = options.index(self)
        return options[(index + 1) % len(options)]

    @property
    def clockwise_previous(self):
        options = list(CardinalDirection)
        index = options.index(self)
        return options[index - 1]


class Vehicle:
    def __init__(self, position: tuple[int, int], direction: CardinalDirection):
        self.position = position
        self.direction = direction

    def rotate_clockwise(self):
        self.direction = self.direction.clockwise_next

    def rotate_counter_clockwise(self):
        self.direction = self.direction.clockwise_previous

    @property
    def forward_position(self) -> tuple[int, int]:
        new_x = self.position[0] + self.direction.vector[0]
        new_y = self.position[1] + self.direction.vector[1]
        return new_x, new_y

    def move_forward(self):
        self.position = self.forward_position


class Rover(Vehicle):
    def __init__(
        self,
        name: str,
        position: tuple[int, int],
        direction: CardinalDirection,
        plateau_dimensions: tuple[int, int],
    ):
        super().__init__(position, direction)
        self.name = name
        self.plateau_dimensions = plateau_dimensions

    def execute_instruction(self, instruction: str):
        if instruction == "M":
            self.move_forward()
        elif instruction == "L":
            self.rotate_clockwise()
        elif instruction == "R":
            self.rotate_counter_clockwise()

    def __str__(self):
        return f"{self.name}: {self.position[0]} {self.position[1]} {self.direction}"
