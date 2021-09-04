import factory

from rover.models import CardinalDirection, Vehicle


class VehicleFactory(factory.Factory):
    class Meta:
        model = Vehicle

    position = (0, 0)
    direction = CardinalDirection.NORTH
