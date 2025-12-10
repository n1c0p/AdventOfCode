import utils
from itertools import combinations
import re

def map_fn(machine:str) -> tuple[str,str,str]:
    indicator_light_diagram, config, joltage = machine.replace("] (","]*(").replace(") {",")*{").split("*")
    return indicator_light_diagram, config, joltage

def parse_machine(indicator_light_diagram:str, config:str):
    # Estrai il pattern target [.##.]
    target_match = re.search(r'\[([.#]+)\]', indicator_light_diagram)
    target = [1 if c == '#' else 0 for c in target_match.group(1)]

    # Estrai i bottoni (0,1,2) etc.
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', config):
        button = [int(x) for x in match.group(1).split(',')]
        buttons.append(button)

    return target, buttons


def solve_machine(target, buttons):
    """Trova il minimo numero di pressioni per una macchina"""
    n_lights = len(target)

    # Prova tutte le combinazioni possibili di bottoni
    # Inizia da 0 bottoni fino a tutti i bottoni
    for n_buttons in range(len(buttons) + 1):
        for combo in combinations(range(len(buttons)), n_buttons):
            # Simula la pressione di questi bottoni
            state = [0] * n_lights
            for button_idx in combo:
                for light_idx in buttons[button_idx]:
                    if light_idx < n_lights:
                        state[light_idx] ^= 1  # XOR toggle

            # Controlla se corrisponde al target
            if state == target:
                return n_buttons

    return float('inf')  # Non trovato (non dovrebbe accadere)

def part_1(machine: list[tuple[str,str,str]]) -> None:
    total_presses = 0

    for line in machine:
        indicator_light_diagram, config, joltage = line
        target, buttons = parse_machine(indicator_light_diagram, config)
        min_presses = solve_machine(target, buttons)
        total_presses += min_presses

    print(f"Result part 1", total_presses)


def part_2(machine: list[tuple[str,str,str]]) -> None:
    result = 0
    print(f"Result part 2", result)

if __name__ == "__main__":
    data = utils.read_input(10, map_fn, True)
    # Esegue entrambe le parti
    part_1(data)
    part_2(data)