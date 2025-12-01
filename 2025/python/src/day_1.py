import utils

def map_fn(line):
    return line

def part_1():
    rotations = utils.read_input(1,map_fn, True)

    pos = 50
    hits = 0

    for rot in rotations:
        direction = rot[0]
        dist = int(rot[1:])

        match direction:
            case "L":
                pos = (pos - dist) % 100
            case "R":
                pos = (pos + dist) % 100

        if pos == 0:
            hits += 1

    print("Password part_1:", hits)

def part_2():
    rotations = utils.read_input(1,map_fn, True)

    pos = 50
    hits = 0

    for rot in rotations:
        direction = rot[0]
        dist = int(rot[1:])

        match direction:
            case "L":
                pos = (pos - dist) % 100
            case "R":
                pos = (pos + dist) % 100

        if pos == 0:
            hits += 1

    print("Password part_2:", hits)

if __name__ == "__main__":
    part_2()