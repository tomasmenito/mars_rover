from unittest import mock

import pytest

from rover.models import CardinalDirection, Rover, Vehicle, VehicleInstruction
from tests.factories import RoverFactory, VehicleFactory


class TestCardinalDirection:
    @pytest.mark.parametrize(
        "direction, expected",
        [
            (CardinalDirection.NORTH, CardinalDirection.EAST),
            (CardinalDirection.EAST, CardinalDirection.SOUTH),
            (CardinalDirection.SOUTH, CardinalDirection.WEST),
            (CardinalDirection.WEST, CardinalDirection.NORTH),
        ],
    )
    def test_cardinal_direction_clockwise_next(self, direction, expected):
        assert direction.clockwise_next == expected

    @pytest.mark.parametrize(
        "direction, expected",
        [
            (CardinalDirection.NORTH, CardinalDirection.WEST),
            (CardinalDirection.WEST, CardinalDirection.SOUTH),
            (CardinalDirection.SOUTH, CardinalDirection.EAST),
            (CardinalDirection.EAST, CardinalDirection.NORTH),
        ],
    )
    def test_cardinal_direction_clockwise_previous(self, direction, expected):
        assert direction.clockwise_previous == expected


class TestVehicle:
    @pytest.mark.parametrize(
        "start_direction, expected",
        [
            (CardinalDirection.NORTH, CardinalDirection.EAST),
            (CardinalDirection.EAST, CardinalDirection.SOUTH),
            (CardinalDirection.SOUTH, CardinalDirection.WEST),
            (CardinalDirection.WEST, CardinalDirection.NORTH),
        ],
    )
    def test_vehicle_rotation_clockwise(self, start_direction, expected):
        v: Vehicle = VehicleFactory(direction=start_direction)
        v.rotate_clockwise()
        assert v.direction == expected

    @pytest.mark.parametrize(
        "start_direction, expected",
        [
            (CardinalDirection.NORTH, CardinalDirection.WEST),
            (CardinalDirection.WEST, CardinalDirection.SOUTH),
            (CardinalDirection.SOUTH, CardinalDirection.EAST),
            (CardinalDirection.EAST, CardinalDirection.NORTH),
        ],
    )
    def test_vehicle_rotation_counter_clockwise(self, start_direction, expected):
        v: Vehicle = VehicleFactory(direction=start_direction)
        v.rotate_counter_clockwise()
        assert v.direction == expected

    @pytest.mark.parametrize(
        "direction, position, expected",
        [
            (CardinalDirection.NORTH, (0, 0), (0, 1)),
            (CardinalDirection.EAST, (0, 0), (1, 0)),
            (CardinalDirection.SOUTH, (0, 0), (0, -1)),
            (CardinalDirection.WEST, (0, 0), (-1, 0)),
        ],
    )
    def test_forward_position(self, direction, position, expected):
        v: Vehicle = VehicleFactory(direction=direction, position=position)
        assert v.forward_position == expected

    def test_move_forward(self, faker):
        position = faker.pyint(), faker.pyint()
        v: Vehicle = VehicleFactory()
        with mock.patch(
            "rover.models.Vehicle.forward_position", return_value=position, new_callable=mock.PropertyMock
        ) as mock_forward_position:
            v.move_forward()
            mock_forward_position.assert_called_once()
        assert v.position == position


class TestVehicleInstruction:
    def test_move_forward(self):
        v: Vehicle = VehicleFactory()
        with mock.patch("rover.models.Vehicle.move_forward") as mock_move_forward:
            VehicleInstruction.MOVE_FORWARD.action(v)
            mock_move_forward.assert_called_once()

    def test_rotate_clockwise(self):
        v: Vehicle = VehicleFactory()
        with mock.patch("rover.models.Vehicle.rotate_clockwise") as mock_rotate_clockwise:
            VehicleInstruction.ROTATE_CLOCKWISE.action(v)
            mock_rotate_clockwise.assert_called_once()

    def test_rotate_counter_clockwise(self):
        v: Vehicle = VehicleFactory()
        with mock.patch("rover.models.Vehicle.rotate_counter_clockwise") as mock_rotate_counter_clockwise:
            VehicleInstruction.ROTATE_COUNTER_CLOCKWISE.action(v)
            mock_rotate_counter_clockwise.assert_called_once()


class TestRover:
    def test_rover_turn_right(self):
        rover: Rover = RoverFactory()

        previous_direction = rover.direction
        rover.execute_instruction(VehicleInstruction.ROTATE_COUNTER_CLOCKWISE)
        assert rover.direction == previous_direction.clockwise_previous

    def test_rover_turn_left(self):
        rover: Rover = RoverFactory()

        previous_direction = rover.direction
        rover.execute_instruction(VehicleInstruction.ROTATE_CLOCKWISE)
        assert rover.direction == previous_direction.clockwise_next

    def test_rover_move_forward(self, faker):
        position = faker.pyint(), faker.pyint()
        rover: Rover = RoverFactory(position=position, direction=CardinalDirection.NORTH)

        previous_position = rover.position
        rover.execute_instruction(VehicleInstruction.MOVE_FORWARD)
        assert rover.position == (previous_position[0], (previous_position[1] + 1))
