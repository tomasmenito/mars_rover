import factory

from rover.models import CardinalDirection, Rover, Vehicle


class VehicleFactory(factory.Factory):
    class Meta:
        model = Vehicle

    position = (0, 0)
    direction = factory.Faker("random_element", elements=list(CardinalDirection))


class RoverFactory(VehicleFactory):
    class Meta:
        model = Rover

    name = factory.Sequence(lambda n: f"Rover {n}")
    plateau_dimensions = (5, 5)
