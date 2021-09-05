import factory

from rover.models import CardinalDirection, RestrictedNavigationVehicle, Rover, Vehicle


class VehicleFactory(factory.Factory):
    class Meta:
        model = Vehicle

    position = (0, 0)
    direction = factory.Faker("random_element", elements=list(CardinalDirection))


class RestrictedNavigationVehicleFactory(VehicleFactory):
    class Meta:
        model = RestrictedNavigationVehicle

    navigable_area = (0, 0)


class RoverFactory(RestrictedNavigationVehicleFactory):
    class Meta:
        model = Rover

    name = factory.Sequence(lambda n: f"Rover {n}")
