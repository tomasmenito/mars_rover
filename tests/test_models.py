from unittest import mock

import pytest

from rover.models import CardinalDirection, Vehicle
from tests.factories import VehicleFactory


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
