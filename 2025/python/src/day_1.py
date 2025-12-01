import utils

def map_fn(line):
    return line

def part_1(rotations):
    zeros = 0
    dial = 50
    for line in rotations:
        step = -1 if line[0] == "L" else 1
        amount = int(line[1:])
        start = dial  # caching starting dial position
        dial = (start + step * amount) % 100

        if dial == 0:
            zeros += 1

    print("Password part_1:", zeros)

def part_2(rotations):
    zeros = 0
    dial = 50
    for line in rotations:
        step = -1 if line[0] == "L" else 1
        amount = int(line[1:])
        start = dial  # caching starting dial position
        dial = (start + step * amount) % 100

        # Each click k moves the dial in position p = (start + step*k) % 100
        # I want to count all the positions p=0
        # These are the solution of:
        # start + step*k = 0 (mod 100)
        # solving for k:
        # k = -start * step^-1 (mod 100)
        # So the first click k that touches 0 is:
        k_first = (-start * pow(step, -1, 100)) % 100

        if k_first == 0:  # k=0 is an invalid configuration, since I want to check dial positions only after a valid click (k>=1)
            k_first = 100  # if by chance k=0, the next valid "landing on zero" is for k=100

        # count zero crossings
        crosszero = 0 if k_first > amount else 1 + (amount - k_first) // 100

        zeros += crosszero

    print("Password part_2:", zeros)



if __name__ == "__main__":
    input_rotations = utils.read_input(1, map_fn, False)
    part_1(input_rotations)
    part_2(input_rotations)