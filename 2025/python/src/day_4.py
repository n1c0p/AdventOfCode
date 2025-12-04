import utils

def map_fn(input_file):
    lines = [line.strip() for line in input_file if '@' in line or '.' in line]
    return lines


def solve(grid):
    rows = len(grid)
    cols = len(grid[0])
    accessible_rolls = 0

    # 2. Itera su ogni cella della griglia.
    for r in range(rows):
        for c in range(cols):
            # 3. Controlla se la cella corrente contiene un rotolo di carta.
            if grid[r][c] == '@':
                adjacent_rolls = 0

                # 4. Itera sulle 8 posizioni adiacenti.
                #    (dr, dc) rappresenta lo spostamento relativo dalla cella corrente.
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Salta la cella stessa (spostamento 0,0).
                        if dr == 0 and dc == 0:
                            continue

                        # Calcola le coordinate del vicino.
                        nr, nc = r + dr, c + dc

                        # Controlla che il vicino sia dentro i bordi della griglia.
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Se il vicino è un rotolo, incrementa il contatore.
                            if grid[nr][nc] == '@':
                                adjacent_rolls += 1

                # 5. Se il numero di rotoli adiacenti è minore di 4,
                #    il rotolo corrente è accessibile.
                if adjacent_rolls < 4:
                    accessible_rolls += 1

    # 6. Stampa il risultato finale.
    print(f"Il numero di rotoli di carta accessibili è: {accessible_rolls}")


def solve_part_two(grid):

    if not grid:
        print("La griglia nel file di input è vuota o non trovata.")
        return

    rows = len(grid)
    cols = len(grid[0])
    total_removed_rolls = 0

    # 2. Inizia un ciclo che continua finché si rimuovono rotoli.
    while True:
        removable_this_round = []

        # 3. Identifica tutti i rotoli attualmente accessibili.
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    adjacent_rolls = 0
                    # Itera sulle 8 posizioni adiacenti.
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue

                            nr, nc = r + dr, c + dc

                            # Controlla i bordi e se il vicino è un rotolo.
                            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                                adjacent_rolls += 1

                    # Se accessibile, aggiungilo alla lista di rimozione.
                    if adjacent_rolls < 4:
                        removable_this_round.append((r, c))

        # 4. Se nessun rotolo è stato rimosso in questo turno, esci dal ciclo.
        if not removable_this_round:
            break

        # 5. Aggiorna il conteggio totale e la griglia.
        total_removed_rolls += len(removable_this_round)
        for r, c in removable_this_round:
            grid[r][c] = '.'  # "Rimuove" il rotolo.

    # 7. Stampa il risultato finale.
    print(f"Il numero totale di rotoli di carta rimovibili è: {total_removed_rolls}")


def part_1(data:list[list[str]]) -> None:
    solve(data)

def part_2(data:list[list[str]]) -> None:
    solve_part_two(data)

if __name__ == "__main__":
    data_input = utils.read_input(4, map_fn, False)
    part_1(data_input)
    part_2(data_input)