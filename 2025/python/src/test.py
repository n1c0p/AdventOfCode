import re
from itertools import combinations


def parse_machine(line):
    """Parse una linea per estrarre target, bottoni e requisiti joltage"""
    # Estrai il pattern target [.##.]
    target_match = re.search(r'\[([.#]+)\]', line)
    target = [1 if c == '#' else 0 for c in target_match.group(1)]

    # Estrai i bottoni (0,1,2) etc.
    buttons = []
    for match in re.finditer(r'\(([0-9,]+)\)', line):
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


def solve_puzzle(input_text):
    """Risolve il puzzle completo"""
    lines = [line.strip() for line in input_text.strip().split('\n') if line.strip()]

    total_presses = 0
    for line in lines:
        target, buttons = parse_machine(line)
        min_presses = solve_machine(target, buttons)
        total_presses += min_presses
        print(f"Macchina: {min_presses} pressioni minime")

    return total_presses


# Test con l'esempio
example = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""

result = solve_puzzle(example)
print(f"\nRisultato totale: {result}")