import re  # Per le espressioni regolari nel parsing
from itertools import combinations  # Per generare combinazioni di bottoni
from ortools.linear_solver import pywraplp  # Solver per problemi di programmazione lineare

import utils  # Modulo personalizzato per leggere gli input

class MachineConfiguration:
    """
    Rappresenta la configurazione di una macchina con bottoni e livelli di voltaggio.
    Risolve il problema di programmazione lineare per trovare il numero minimo di pressioni.
    """

    def __init__(self, toggles: list[list[int]], joltages: list[int]):
        """
        Inizializza la configurazione della macchina.

        Args:
            toggles: Lista di bottoni, dove ogni bottone è una lista di indici che influenza
            joltages: Lista dei livelli di voltaggio target per ogni posizione
        """
        # Converte joltages in tupla (immutabile) per garantire che non venga modificato
        self.joltages = tuple(joltages)
        self.toggles = []

        # Converte ogni bottone in una rappresentazione binaria
        # Esempio: se toggle = [0, 2] e ci sono 4 joltages, diventa [1, 0, 1, 0]
        for toggle in toggles:
            # Crea un array binario: 1 se l'indice è nel toggle, 0 altrimenti
            binary_toggle = [int(i in toggle) for i, _ in enumerate(self.joltages)]
            self.toggles.append(binary_toggle)

        # Ordina i bottoni in ordine decrescente per numero di effetti
        # (bottoni che influenzano più posizioni vengono prima)
        self.toggles = sorted(self.toggles, key=lambda x: -sum(x))

    def solve_with_linear_solver(self) -> tuple[int]:
        """
        Risolve il problema di programmazione lineare intera per trovare il numero minimo
        di pressioni dei bottoni necessarie per raggiungere i livelli di voltaggio target.

        Returns:
            Il numero minimo totale di pressioni dei bottoni
        """
        # Numero di variabili = numero di bottoni disponibili
        number_of_variables = len(self.toggles)
        # Numero di vincoli = numero di posizioni di voltaggio
        number_of_constraints = len(self.joltages)

        # Crea un solver SCIP (ottimizzatore per problemi di programmazione lineare intera)
        solver = pywraplp.Solver.CreateSolver("SCIP")

        # Crea una variabile intera non negativa per ogni bottone
        # x[k] rappresenta quante volte il bottone k viene premuto
        x = [
            solver.IntVar(0, solver.infinity(), f"x_{k}")
            for k in range(number_of_variables)
        ]

        # Aggiungi un vincolo per ogni posizione di voltaggio
        for j in range(number_of_constraints):
            # La somma degli effetti di tutti i bottoni sulla posizione j
            # deve essere uguale al voltaggio target per quella posizione
            # Equazione: Σ(toggles[k][j] * x[k]) = joltages[j]
            solver.Add(
                sum(self.toggles[k][j] * x[k] for k in range(number_of_variables))
                == self.joltages[j]
            )

        # Obiettivo: minimizzare il numero totale di pressioni dei bottoni
        solver.Minimize(solver.Sum(x))

        # Risolve il problema di ottimizzazione
        status = solver.Solve()

        # Verifica se è stata trovata una soluzione ottimale
        if status == pywraplp.Solver.OPTIMAL:
            # Restituisce il valore ottimale (numero minimo di pressioni)
            return solver.Objective().Value()
        else:
            # Se non esiste una soluzione, solleva un'eccezione
            print("No solution found.")
            raise ValueError

def map_fn(machine: str) -> tuple[str, str, str]:
    """
    Divide una stringa di input della macchina in tre componenti.

    Args:
        machine: Stringa nel formato "[.##.] (0,1) {1,2,3}"

    Returns:
        Tupla contenente (diagramma_luci, configurazione_bottoni, voltaggi)
    """
    # Sostituisce "] (" con "]*(" e ") {" con ")*{" per creare delimitatori unici
    # poi divide la stringa usando "*" come separatore
    indicator_light_diagram, config, joltage = machine.replace("] (", "]*(").replace(") {", ")*{").split("*")
    return indicator_light_diagram, config, joltage


def parse_machine(indicator_light_diagram: str, config: str, joltage: str) -> tuple[list[int], list[list[int]], list[int]]:
    """
    Estrae i dati strutturati dalle stringhe di input della macchina.

    Args:
        indicator_light_diagram: Stringa tipo "[.##.]" che rappresenta lo stato target delle luci
        config: Stringa tipo "(0,1)(2,3)" che rappresenta quali luci ogni bottone influenza
        joltage: Stringa tipo "{1,2,3}" che rappresenta i livelli di voltaggio target

    Returns:
        Tupla contenente (stato_target, configurazione_bottoni, livelli_voltaggio)
    """
    # Estrai il pattern target dalle parentesi quadre [.##.]
    # Cerca una sequenza di '.' e '#' tra parentesi quadre
    target_match = re.search(r'\[([.#]+)]', indicator_light_diagram)
    # Converte in lista binaria: '#' -> 1 (luce accesa), '.' -> 0 (luce spenta)
    target = [1 if item == '#' else 0 for item in target_match.group(1)]

    # Estrai i bottoni dalle parentesi tonde (0,1,2) etc.
    # Ogni gruppo di numeri tra parentesi rappresenta gli indici delle luci che un bottone influenza
    buttons = [[int(x) for x in match.group(1).split(',')] for match in re.finditer(r'\(([0-9,]+)\)', config)]

    # Estrai i livelli di voltaggio dalle parentesi graffe {0,1,2} etc.
    # Converte tutti i numeri separati da virgole in una lista di interi
    joltage_levels = [int(x) for match in re.finditer(r'\{([0-9,]+)}', joltage) for x in match.group(1).split(',')]

    return target, buttons, joltage_levels

def solve_machine(target, buttons):
    """
    Trova il minimo numero di pressioni dei bottoni necessarie per raggiungere lo stato target.
    Utilizza un approccio a forza bruta testando tutte le combinazioni possibili.

    Args:
        target: Lista binaria che rappresenta lo stato desiderato delle luci
        buttons: Lista di liste, dove ogni lista contiene gli indici delle luci influenzate da un bottone

    Returns:
        Il numero minimo di bottoni da premere (ogni bottone premuto una sola volta)
    """
    # Numero totale di luci nella macchina
    n_lights = len(target)

    # Prova tutte le combinazioni possibili di bottoni
    # Inizia da 0 bottoni fino a tutti i bottoni disponibili
    for n_buttons in range(len(buttons) + 1):
        # Genera tutte le combinazioni di n_buttons bottoni dalla lista di bottoni
        for combo in combinations(range(len(buttons)), n_buttons):
            # Simula la pressione di questi bottoni
            # Inizializza lo stato con tutte le luci spente
            state = [0] * n_lights

            # Per ogni bottone nella combinazione corrente
            for button_idx in combo:
                # Per ogni luce influenzata da questo bottone
                for light_idx in buttons[button_idx]:
                    # Verifica che l'indice sia valido
                    if light_idx < n_lights:
                        # XOR toggle: inverte lo stato della luce
                        # 0 -> 1 (spenta -> accesa), 1 -> 0 (accesa -> spenta)
                        state[light_idx] ^= 1

            # Controlla se lo stato corrente corrisponde al target
            if state == target:
                # Trovata la soluzione con il minor numero di pressioni
                return n_buttons

    # Non dovrebbe mai arrivare qui se il puzzle ha una soluzione
    return float('inf')  # Infinito indica che non è stata trovata una soluzione


def part_1(machines: list[tuple[str, str, str]]) -> None:
    """
    Risolve la parte 1 del puzzle: trova il numero totale di pressioni di bottoni
    necessarie per tutte le macchine usando l'approccio a forza bruta.

    Args:
        machines: Lista di tuple, ognuna contenente (diagramma_luci, configurazione, voltaggio)
    """
    # Contatore per il numero totale di pressioni di tutti i bottoni
    total_presses = 0

    # Per ogni macchina nell'input
    for machine in machines:
        # Separa i tre componenti della macchina
        indicator_light_diagram, config, joltage = machine

        # Parsing dei componenti per estrarre i dati strutturati
        # target: stato desiderato delle luci
        # buttons: quali luci ogni bottone influenza
        # joltage_level: livelli di voltaggio (non usati nella parte 1)
        target, buttons, joltage_level = parse_machine(indicator_light_diagram, config, joltage)

        # Trova il numero minimo di pressioni per questa macchina
        min_presses = solve_machine(target, buttons)

        # Aggiungi al totale
        total_presses += min_presses

    # Stampa il risultato finale
    print(f"Result part 1", total_presses)


def part_2(machines: list[tuple[str, str, str]]) -> None:
    """
    Risolve la parte 2 del puzzle: trova il numero totale di pressioni di bottoni
    necessarie per tutte le macchine usando la programmazione lineare intera.

    Args:
        machines: Lista di tuple, ognuna contenente (diagramma_luci, configurazione, voltaggio)
    """
    # Lista per contenere le configurazioni di tutte le macchine
    manuals: list[MachineConfiguration] = []

    # Per ogni macchina nell'input
    for machine in machines:
        # Separa i tre componenti della macchina
        indicator_light_diagram, config, joltage = machine

        # Parsing dei componenti per estrarre i dati strutturati
        # target: stato desiderato delle luci (non usato nella parte 2)
        # buttons: quali posizioni ogni bottone influenza
        # joltage_level: livelli di voltaggio target
        target, buttons, joltage_level = parse_machine(indicator_light_diagram, config, joltage)

        # Crea una configurazione macchina per il solver di programmazione lineare
        # Questa usa i livelli di voltaggio invece dello stato binario delle luci
        manuals.append(MachineConfiguration(buttons, joltage_level))

    # Lista per memorizzare le soluzioni di ogni macchina
    solutions = []

    # Risolvi ogni macchina usando il solver di programmazione lineare
    for manual in manuals:
        # Trova il numero minimo di pressioni usando l'ottimizzatore
        pushes = manual.solve_with_linear_solver()
        # Aggiungi alla lista delle soluzioni
        solutions.append(pushes)

    # Calcola la somma totale di tutte le pressioni e stampala
    # int() per convertire da float a intero
    print(f"Result part 2: {int(sum(solutions))}")


if __name__ == "__main__":
    # Legge i dati di input per il giorno 10
    # map_fn viene usata per processare ogni linea dell'input
    # False = usa l'input reale (day_10.txt), True = usa l'esempio (day_10_example.txt)
    data = utils.read_input(10, map_fn, False)

    # Esegue la parte 1: approccio a forza bruta con combinazioni
    part_1(data)

    # Esegue la parte 2: approccio con programmazione lineare intera
    part_2(data)