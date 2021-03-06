import logging
import re
from collections import defaultdict
from typing import Iterable

import click

from rover.exceptions import PositionOutOfNavigableAreaError
from rover.models import CardinalDirection, Rover, VehicleInstruction

logger = logging.getLogger()
PLATEAU_RE = re.compile(r"Plateau:(?P<width>\d)\s*(?P<height>\d)")
ROVER_LANDING_RE = re.compile(r"(?P<name>\w+)\s*Landing:(?P<x>\d+)\s*(?P<y>\d+)\s*(?P<direction>[NESW])")
ROVER_INSTRUCTIONS_RE = re.compile(r"(?P<name>\w+)\s*Instructions:(?P<instructions>[MRL]+)")


@click.command()
@click.argument("input-file", required=True, type=click.File(mode="r"))
def parse_input(input_file):
    plateau_dimensions = None
    rovers_data = defaultdict(dict)

    for line in input_file.readlines():
        if not line:
            continue
        elif match := PLATEAU_RE.match(line):
            plateau_dimensions = int(match["width"]), int(match["height"])
            click.secho(f"Parsed plateau dimensions {plateau_dimensions}", fg="green")
        elif match := ROVER_LANDING_RE.match(line):
            rover_name = match["name"]
            position = (int(match["x"]), int(match["y"]))
            rovers_data[rover_name].update(
                {"name": rover_name, "position": position, "direction": match["direction"]}
            )
            click.secho(
                f"Parsed {rover_name} with position {position} and direction {match['direction']}", fg="green"
            )
        elif match := ROVER_INSTRUCTIONS_RE.match(line):
            rover_name = match["name"]
            rovers_data[rover_name].update({"name": rover_name, "instructions": match["instructions"]})
            click.secho(f"Parsed instructions {match['instructions']} for {rover_name}", fg="green")
        else:
            click.secho(f"Could not parse intruction: {line}", err=True, fg="red")

    if len(rovers_data) == 0 or not plateau_dimensions:
        click.secho("Could not mount valid scenario", err=True, fg="red")
        return
    for rover in process_scenario(rovers_data, plateau_dimensions):
        click.secho(
            f"{rover.name} terminal position: {rover.position[0]} {rover.position[1]} {rover.direction.sign}",
            fg="blue",
        )


def process_scenario(rovers_data, plateau_dimensions) -> Iterable[Rover]:
    for rover_name, data in rovers_data.items():
        rover = Rover(
            name=rover_name,
            position=data["position"],
            direction=CardinalDirection(data["direction"]),
            navigable_area=plateau_dimensions,
        )

        for instruction_sign in data.get("instructions", []):
            instruction = VehicleInstruction(instruction_sign)
            try:
                rover.execute_instruction(instruction)
            except PositionOutOfNavigableAreaError as e:
                logger.warning(f"Could not execute instruction {instruction} due to {e}")

        yield rover


if __name__ == "__main__":
    parse_input()
