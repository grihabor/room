import os
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


def get_start(path):
    arr = Coord([0], [0])

    for x, y in path:
        arr.x.append(arr.x[-1] + x)
        arr.y.append(arr.y[-1] + y)

    pprint(list(zip(arr.x, arr.y)))

    return -min(arr.x), -min(arr.y)


def create_walls(walls):
    path = Path()
    path.push('M', get_start(walls))
    for coords in walls:
        path.push('l', *coords)
    return path


def main():
    with open(FILE_MEASUREMENTS) as f:
        measurements = json.load(f)

    room = svgwrite.Drawing(FILE_DRAWING)
    room.add(create_walls(measurements['walls']))
    room.save(pretty=True)

    
if __name__ == '__main__':
    main()
