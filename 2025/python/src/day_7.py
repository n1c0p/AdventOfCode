import utils

def count_beam_splits(grid):
    """Conta quante volte un raggio viene diviso da splitter ('^') nella griglia."""
    # Ottiene le dimensioni della griglia
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Cerca la posizione iniziale 'S' nella prima riga
    start_col = -1
    for col in range(cols):
        if grid[0][col] == 'S':
            start_col = col
            break

    # Se non trova 'S', restituisce 0
    if start_col == -1:
        return 0

    # Lista dei raggi attualmente attivi, rappresentati come tuple (riga, colonna)
    active_beams = [(0, start_col)]
    # Set per tracciare le posizioni già visitate ed evitare duplicati
    visited = set()
    # Contatore del numero di split
    split_count = 0

    # Continua finché ci sono raggi attivi
    while active_beams:
        new_beams = []

        # Processa ogni raggio attivo
        for row, col in active_beams:
            # Muove il raggio verso il basso di una riga
            row += 1

            # Se il raggio esce dal manifold (oltre l'ultima riga), lo ignora
            if row >= rows:
                continue

            # Controlla cosa c'è nella posizione corrente
            if grid[row][col] == '^':
                # Trovato uno splitter: incrementa il contatore
                split_count += 1

                # Crea due nuovi raggi: uno a sinistra e uno a destra
                if col > 0:
                    beam_left = (row, col - 1)
                    if beam_left not in visited:
                        new_beams.append(beam_left)
                        visited.add(beam_left)

                if col < cols - 1:
                    beam_right = (row, col + 1)
                    if beam_right not in visited:
                        new_beams.append(beam_right)
                        visited.add(beam_right)
            else:
                # Spazio vuoto: il raggio continua dritto
                beam = (row, col)
                if beam not in visited:
                    new_beams.append(beam)
                    visited.add(beam)

        # Aggiorna i raggi attivi per la prossima iterazione
        active_beams = new_beams

    return split_count

def count_quantum_timelines(grid):
    """Conta il numero totale di timeline quantistiche che raggiungono l'uscita."""
    # Ottiene le dimensioni della griglia
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Cerca la posizione iniziale 'S' nella prima riga
    start_col = -1
    for col in range(cols):
        if grid[0][col] == 'S':
            start_col = col
            break

    if start_col == -1:
        return 0

    # Dizionario che mappa ogni posizione al numero di timeline che la attraversano
    # Inizialmente: 1 timeline parte dalla posizione 'S'
    current_states = {(0, start_col): 1}

    # Processa ogni riga della griglia
    for row in range(rows):
        next_states = {}

        # Per ogni posizione con le sue timeline
        for (r, c), count in current_states.items():
            # Considera solo le posizioni nella riga corrente
            if r != row:
                continue

            # Calcola la prossima riga
            next_row = row + 1

            # Se la prossima riga esce dal manifold
            if next_row >= rows:
                # Conta queste timeline come uscite
                if 'exit' not in next_states:
                    next_states['exit'] = 0
                next_states['exit'] += count
                continue

            # Controlla il contenuto della cella successiva
            if grid[next_row][c] == '^':
                # Splitter: ogni timeline si divide in due
                # Una va a sinistra
                if c > 0:
                    key = (next_row, c - 1)
                    next_states[key] = next_states.get(key, 0) + count

                # Una va a destra
                if c < cols - 1:
                    key = (next_row, c + 1)
                    next_states[key] = next_states.get(key, 0) + count
            else:
                # Spazio vuoto: le timeline continuano nella stessa colonna
                key = (next_row, c)
                next_states[key] = next_states.get(key, 0) + count

        # Aggiorna gli stati per la prossima iterazione
        current_states = next_states

    # Restituisce il numero totale di timeline che hanno raggiunto l'uscita
    return current_states.get('exit', 0)

def create_grid(lines: list[str]):
    """Estrae la griglia dall'input, iniziando dalla riga che contiene 'S'."""
    grid = []
    reading_grid = False
    for line in lines:
        # Rimuove il newline finale
        line = line.rstrip('\n')
        # Inizia a leggere quando trova 'S' o se ha già iniziato
        if 'S' in line or reading_grid:
            reading_grid = True
            # Aggiunge la riga se non è vuota e non è un separatore
            if line and not line.startswith('---'):
                grid.append(line)
    return grid

def part_1(data_input: list[str]) -> None:
    """Risolve la parte 1: conta gli split del raggio."""
    grid = create_grid(data_input)
    result = count_beam_splits(grid)
    print(f"Il raggio viene diviso {result} volte")

def part_2(data_input: list[str]) -> None:
    """Risolve la parte 2: conta le timeline quantistiche totali."""
    grid = create_grid(data_input)
    result_p2 = count_quantum_timelines(grid)
    print(f"Numero totale di timeline: {result_p2}")

if __name__ == "__main__":
    # Legge l'input del giorno 7
    data = utils.read_input_str(7, str, True)
    # Esegue entrambe le parti
    part_1(data)
    part_2(data)