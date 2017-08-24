import os
from operator import attrgetter
from pprint import pprint

import svgwrite
from svgwrite.path import Path
import json


DIR_SRC = os.path.split(os.path.abspath(__file__))[0]
DIR_ROOT = os.path.normpath(os.path.join(DIR_SRC, os.pardir))

DIR_DATA = os.path.join(DIR_ROOT, 'data')
FILE_MEASUREMENTS = os.path.join(DIR_DATA, 'measurements.json')
FILE_DRAWING = os.path.join(DIR_DATA, 'room.svg')


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coord(self.x + other.x,
                     self.y + other.y)

    def __repr__(self):
        return '({0.x}, {0.y})'.format(self)


def rel_to_abs(path):
    """Convert relative coordinates to absolute"""
    arr = [Coord(0, 0)]

    for point in path:
        rel = Coord(*point['rel'])
        arr.append(arr[-1] + rel)

    pprint(arr)
    return arr


def create_walls(walls):
    abs_coords = rel_to_abs(walls)
    start = Coord(-min(abs_coords, key=attrgetter('x')).x,
                  -min(abs_coords, key=attrgetter('y')).y)

    path = Path()
    path.push('M', start.x, start.y)
    for coords in abs_coords:
        path.push('L',
                  start.x + coords.x,
                  start.y + coords.y)
    return path


def main():
    with open(FILE_MEASUREMENTS) as f:
        measurements = json.load(f)

    room = svgwrite.Drawing(FILE_DRAWING)
    room.add(create_walls(measurements['walls']))
    room.save(pretty=True)

    
if __name__ == '__main__':
    main()
