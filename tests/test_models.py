import pytest

from rover.models import CardinalDirection


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
