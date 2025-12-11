import utils  # Modulo personalizzato per leggere gli input
from collections import deque

def map_fn(line_devices: str) -> tuple[str, set[str]]:
    parent, children = line_devices.strip().split(":")
    children = set(children.strip(" ").split(" "))
    return parent, children

def create_dictionary(list_of_devices: list[tuple[str, set[str]]]) -> dict[str, set[str]]:
    circuit = {}
    for device in list_of_devices:
        circuit[device[0]] = device[1]
    return circuit

def part_1(list_of_devices: list[tuple[str, set[str]]]) -> None:
    # Stampa il risultato finale
    circuit = create_dictionary(list_of_devices)
    paths = 0
    frontier = deque(["you"])
    while frontier:
        node = frontier.popleft()
        if node == "out":
            paths += 1

        for next_node in circuit.get(node, set()):
            frontier.append(next_node)

    print(f"Result part 1 ->", paths)


def part_2(machines: list[tuple[str, str, str]]) -> None:
    # Lista per memorizzare le soluzioni di ogni macchina
    solutions = []
    print(f"Result part 2: {int(sum(solutions))}")


if __name__ == "__main__":
    data = utils.read_input(11, map_fn, True)
    part_1(data)
    # Esegue la parte 2: approccio con programmazione lineare intera
    #part_2(data)
