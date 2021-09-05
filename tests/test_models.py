from contextlib import nullcontext as does_not_raise
from unittest import mock

import pytest

from rover.exceptions import PositionOutOfNavigableAreaError
from rover.models import CardinalDirection, RestrictedNavigationVehicle, Rover, Vehicle, VehicleInstruction
from tests.factories import RestrictedNavigationVehicleFactory, RoverFactory, VehicleFactory


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
        navigable_area = position[0] + 2, position[1] + 2
        rover: Rover = RoverFactory(
            position=position, direction=CardinalDirection.NORTH, navigable_area=navigable_area
        )

        previous_position = rover.position
        rover.execute_instruction(VehicleInstruction.MOVE_FORWARD)
        assert rover.position == (previous_position[0], (previous_position[1] + 1))


class TestRestrictedNavigationVehicle:
    @pytest.mark.parametrize(
        "is_navigable, expected",
        [
            (True, does_not_raise()),
            (False, pytest.raises(PositionOutOfNavigableAreaError)),
        ],
    )
    def test_move_forward(self, is_navigable, expected):
        v: RestrictedNavigationVehicle = RestrictedNavigationVehicleFactory()
        with mock.patch(
            "rover.models.RestrictedNavigationVehicle.is_navigable", return_value=is_navigable
        ) as mock_is_navigable:
            with expected:
                v.move_forward()
            mock_is_navigable.assert_called_once()

    @pytest.mark.parametrize(
        "position, navigable_area, expected",
        [
            ((0, 0), (1, 1), True),
            ((10, 10), (15, 15), True),
            ((1, 0), (1, 1), False),
            ((0, 1), (1, 1), False),
            ((0, 0), (0, 0), False),
        ],
    )
    def test_is_navigable(self, position, navigable_area, expected):
        v: RestrictedNavigationVehicle = RestrictedNavigationVehicleFactory(navigable_area=navigable_area)
        assert v.is_navigable(position) is expected
