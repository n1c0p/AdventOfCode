import re
from itertools import combinations
from ortools.linear_solver import pywraplp

import utils

class MachineConfiguration:
    def __init__(self, toggles: list[list[int]], joltages: list[int]):
        self.joltages = tuple(joltages)
        self.toggles = []
        for toggle in toggles:
            binary_toggle = [int(i in toggle) for i, _ in enumerate(self.joltages)]
            self.toggles.append(binary_toggle)
        self.toggles = sorted(self.toggles, key=lambda x: -sum(x))

    def solve_linear_solver(self) -> tuple[int]:
        number_of_variables = len(self.toggles)
        number_of_constraints = len(self.joltages)

        solver = pywraplp.Solver.CreateSolver("SCIP")  # SCIP is included in OR-Tools

        x = [
            solver.IntVar(0, solver.infinity(), f"x_{k}")
            for k in range(number_of_variables)
        ]

        for j in range(number_of_constraints):
            solver.Add(
                sum(self.toggles[k][j] * x[k] for k in range(number_of_variables))
                == self.joltages[j]
            )
        solver.Minimize(solver.Sum(x))
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return solver.Objective().Value()
        else:
            print("No solution found.")
            raise ValueError

def map_fn(machine: str) -> tuple[str, str, str]:
    indicator_light_diagram, config, joltage = machine.replace("] (", "]*(").replace(") {", ")*{").split("*")
    return indicator_light_diagram, config, joltage


def parse_machine(indicator_light_diagram: str, config: str, joltage: str) -> tuple[list[int], list[list[int]], list[int]]:
    # Estrai il pattern target [.##.]
    target_match = re.search(r'\[([.#]+)]', indicator_light_diagram)
    target = [1 if item == '#' else 0 for item in target_match.group(1)]

    # Estrai i bottoni (0,1,2) etc.
    buttons = [[int(x) for x in match.group(1).split(',')] for match in re.finditer(r'\(([0-9,]+)\)', config)]

    # Estrai i livelli di voltaggio (0,1,2) etc.
    joltage_levels = [int(x) for match in re.finditer(r'\{([0-9,]+)}', joltage) for x in match.group(1).split(',')]

    return target, buttons, joltage_levels

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


def part_1(machines: list[tuple[str, str, str]]) -> None:
    total_presses = 0
    for machine in machines:
        indicator_light_diagram, config, joltage = machine
        target, buttons, joltage_level = parse_machine(indicator_light_diagram, config, joltage)
        min_presses = solve_machine(target, buttons)
        total_presses += min_presses

    print(f"Result part 1", total_presses)


def part_2(machines: list[tuple[str, str, str]]) -> None:
    manuals: list[MachineConfiguration] = []
    for machine in machines:
        indicator_light_diagram, config, joltage = machine
        target, buttons, joltage_level = parse_machine(indicator_light_diagram, config, joltage)
        manuals.append(MachineConfiguration(buttons, joltage_level))

    solutions = []
    for manual in manuals:
        pushes = manual.solve_linear_solver()
        solutions.append(pushes)

    print(f"Result part 2: {int(sum(solutions))}")


if __name__ == "__main__":
    data = utils.read_input(10, map_fn, False) # True per esempio, False per input reale
    # Esegue entrambe le parti
    part_1(data)
    part_2(data)