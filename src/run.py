import svgwrite
import json

FILE_MEASUREMENTS = 'measurements.json'


def main():
    with open(FILE_MEASUREMENTS) as f:
        measurements = json.load(f)
    
    room = svgwrite.Drawing('room.svg')
	room.add    
    
    
if __name__ == '__main__':
    main()
