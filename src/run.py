import os
from collections import defaultdict
from operator import attrgetter
from pprint import pprint
from typing import List

import svgwrite
from svgwrite.path import Path
import json

from svgwrite.shapes import Line

DIR_SRC = os.path.split(os.path.abspath(__file__))[0]
DIR_ROOT = os.path.normpath(os.path.join(DIR_SRC, os.pardir))

DIR_DATA = os.path.join(DIR_ROOT, 'data')
FILE_MEASUREMENTS = os.path.join(DIR_DATA, 'measurements.json')
FILE_DRAWING = os.path.join(DIR_DATA, 'room.svg')


class Coord:
    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __add__(self, other):
        return Coord(self.x + other.x,
                     self.y + other.y,
                     name=self.name)

    def __repr__(self):
        return '<Coord "{0.name}": {0.x}, {0.y}>'.format(self)


def rel_to_abs(path):
    """Convert relative coordinates to absolute"""
    arr = [Coord(0, 0, name='start')]

    for point in path:
        rel = Coord(*point['rel'], name=None if 'id' not in point else point['id'])
        abs_coords = rel + arr[-1]
        abs_coords.name = rel.name
        arr.append(abs_coords)

    # pprint(arr)
    return arr


def create_walls(walls: List[Coord], start):
    path = Path()
    path.push('M', start.x, start.y)
    for coords in walls:
        path.push('L', coords.x, coords.y)
    return path


def create_doors(doors, walls):
    door_ids = set()
    door_coords = defaultdict(list)
    for door_point_id in doors:
        door_id, index = door_point_id[0].split(':')
        door_ids.add(door_id)

    for point in walls:
        if point.name is None or point.name.find(':') == -1:
            continue

        name_id, index = point.name.split(':')
        if name_id in door_ids:
            door_coords[name_id].append(point)

    lines = []
    for door_id, door_pair in door_coords.items():
        assert len(door_pair) == 2
        print('Create door {}'.format(door_id))
        start = door_pair[0].x, door_pair[0].y
        end = door_pair[1].x, door_pair[1].y
        lines.append(Line(start, end))

    return lines


def main():
    with open(FILE_MEASUREMENTS) as f:
        measurements = json.load(f)

    walls_abs = rel_to_abs(measurements['walls'])

    start = Coord(-min(walls_abs, key=attrgetter('x')).x,
                  -min(walls_abs, key=attrgetter('y')).y)

    walls_abs = [coords + start for coords in walls_abs]

    room = svgwrite.Drawing(FILE_DRAWING)
    room.add(create_walls(walls_abs, start))
    for line in create_doors(measurements['doors'], walls_abs):
        room.add(line)
    room.save(pretty=True)

    
if __name__ == '__main__':
    main()
