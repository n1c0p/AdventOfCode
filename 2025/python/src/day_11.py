import utils  # Modulo personalizzato per leggere gli input
from collections import deque

def map_fn(line_devices: str) -> tuple[str, set[str]]:
    # Divide la riga in genitore e figli usando ":" come separatore
    parent, children = line_devices.strip().split(":")
    # Converte i figli in un set, rimuovendo spazi extra
    children = set(children.strip(" ").split(" "))
    return parent, children


def create_graph(list_of_devices: list[tuple[str, set[str]]]) -> dict[str, set[str]]:
    # Crea un dizionario, per rappresentare un grafo, dove ogni dispositivo (chiave) punta ai suoi figli (set di nodi)
    circuit = {}
    for device in list_of_devices:
        circuit[device[0]] = device[1]
    return circuit


# DFS (Depth-First Search) per tracciare tutti i percorsi possibili.
def dfs(circuit, start, end, cache) -> int:
    # Controlla se il risultato è già in cache per evitare ricalcoli
    if (start, end) in cache:
        return cache[(start, end)]

    # Caso base: se siamo arrivati alla destinazione, c'è 1 percorso
    if start == end:
        return 1

    # Somma ricorsivamente tutti i percorsi possibili dai nodi figli
    possibilities = sum([dfs(circuit, node, end, cache) for node in circuit.get(start, {})])

    # Memorizza il risultato nella cache
    cache[(start, end)] = possibilities
    return possibilities


def part_1(list_of_devices):
    # Crea il grafo del circuito
    circuit = create_graph(list_of_devices)
    paths = 0

    # BFS usando una coda (deque) partendo da "you"
    frontier = deque(["you"])

    while frontier:
        node = frontier.popleft()  # Estrae il primo nodo dalla coda

        # Se raggiungiamo "out", incrementa contatore
        if node == "out":
            paths += 1

        # Aggiunge tutti i nodi figli alla coda
        for next_node in circuit.get(node, set()):
            frontier.append(next_node)

    print(f"Result part 1 -> {paths} paths")


def part_2(list_of_devices):
    circuit = create_graph(list_of_devices)
    cache = {}

    # Calcola i percorsi da "svr" a "fft" e "dac"
    path_from_server_to_fft = dfs(circuit, "svr", "fft", cache)
    path_server_to_dac = dfs(circuit, "svr", "dac", cache)

    # Sceglie il percorso più breve e calcola il totale moltiplicando i segmenti
    if path_from_server_to_fft < path_server_to_dac:
        # Percorso: svr → fft → dac → out
        path_fft_to_dac = dfs(circuit, "fft", "dac", cache)
        path_dac_to_out = dfs(circuit, "dac", "out", cache)
        total = path_from_server_to_fft * path_fft_to_dac * path_dac_to_out
    else:
        # Percorso: svr → dac → fft → out
        path_dac_to_fft = dfs(circuit, "dac", "fft", cache)
        path_fft_to_out = dfs(circuit, "fft", "out", cache)
        total = path_server_to_dac * path_dac_to_fft * path_fft_to_out

    print(f"Result part 2 -> {total} paths")


if __name__ == "__main__":
    data = utils.read_input(11, map_fn, False)
    part_1(data)
    part_2(data)