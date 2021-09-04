class Vehicle:
    def __init__(self, position: tuple[int, int], direction: str):
        self.position = position
        self.direction = direction

    def rotate(self, clockwise: bool):
        seq = "NESW"
        current_index = seq.index(self.direction)
        increment = 1 if clockwise else -1

        new_index = (current_index + increment) % len(seq)

        self.direction = seq[new_index]

    def move(self):
        move_directions = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

        delta_x, delta_y = move_directions[self.direction]
        self.position = self.position[0] + delta_x, self.position[1] + delta_y


class Rover(Vehicle):
    def __init__(
        self, name: str, position: tuple[int, int], direction: str, plateau_dimensions: tuple[int, int]
    ):
        super().__init__(position, direction)
        self.name = name
        self.plateau_dimensions = plateau_dimensions

    def execute_instruction(self, instruction: str):
        if instruction == "M":
            self.move()
        elif instruction == "L":
            self.rotate(clockwise=False)
        elif instruction == "R":
            self.rotate(clockwise=True)

    def __str__(self):
        return f"{self.name}: {self.position[0]} {self.position[1]} {self.direction}"
