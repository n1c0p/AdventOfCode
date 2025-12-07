import utils


def map_fn(input_file) -> list[list[str]]:
    """Funzione di mapping per parsare l'input della parte 1."""
    # Divide l'input in parole/token separati da spazi e rimuove gli spazi extra
    problems = [line.strip() for line in input_file.split()]
    return problems


def part_1(problems: list[list[str]]) -> None:
    """Risolve la parte 1: calcola operazioni su colonne di numeri."""
    # Separa i numeri (tutte le righe tranne l'ultima) dagli operatori (ultima riga)
    list_of_number = problems[:-1]
    list_of_operator = problems[-1]

    results = []
    # Itera su ogni operatore (che corrisponde a una colonna)
    for i, operator in enumerate(list_of_operator):
        if operator == '+':
            # Somma tutti i numeri della colonna i-esima
            result = sum(int(row[i]) for row in list_of_number)
        else:  # operator == '*'
            # Moltiplica tutti i numeri della colonna i-esima
            result = 1
            for row in list_of_number:
                result *= int(row[i])
        # Aggiunge il risultato della colonna alla lista
        results.append(result)

    # Somma tutti i risultati parziali e stampa
    print("Result:", sum(results))


def parse_worksheet(lines):
    """Prepara il foglio di lavoro rimuovendo righe vuote e normalizzando la larghezza."""
    # Rimuove gli spazi finali e le righe completamente vuote
    lines = [line.rstrip() for line in lines if line.strip()]

    # Trova la lunghezza della riga più lunga
    max_width = max(len(line) for line in lines)

    # Aggiunge spazi a destra per portare tutte le righe alla stessa lunghezza
    lines = [line.ljust(max_width) for line in lines]

    return lines


def part_2(data: list[str]) -> None:
    """Risolve la parte 2: legge problemi separati da colonne vuote, da destra a sinistra."""
    # Prepara il foglio di lavoro normalizzando le righe
    lines = parse_worksheet(data)
    height = len(lines)
    width = len(lines[0])

    problems = []
    current_problem = []

    # Legge le colonne da destra a sinistra
    for col in range(width - 1, -1, -1):
        # Estrae tutti i caratteri della colonna corrente
        column = [lines[row][col] for row in range(height)]

        # Se la colonna è completamente vuota, è un separatore tra problemi
        if all(c == ' ' for c in column):
            if current_problem:
                # Salva il problema corrente e inizia uno nuovo
                problems.append(current_problem)
                current_problem = []
        else:
            # Aggiunge la colonna al problema corrente
            current_problem.append(column)

    # Aggiunge l'ultimo problema se presente
    if current_problem:
        problems.append(current_problem)

    total = 0
    # Processa ogni problema trovato
    for problem in problems:
        # L'operatore è l'ultimo carattere dell'ultima colonna del problema
        operator = problem[-1][-1]
        numbers = []

        # Estrae i numeri da ogni colonna
        for col in problem:
            # Unisce i caratteri della colonna in una stringa
            num_str = ''.join(col).strip()
            if num_str:
                # Rimuove gli operatori e converte in intero
                app = num_str.replace('+', '').replace('*', '')
                numbers.append(int(app))

        # Calcola il risultato del problema
        result = numbers[0]
        for num in numbers[1:]:
            if operator == '+':
                result += num
            elif operator == '*':
                result *= num

        # Somma al totale
        total += result

    print("Result part 2:", total)


if __name__ == "__main__":
    # Legge l'input per la parte 1 usando una funzione di mapping personalizzata
    data_part_1 = utils.read_input(6, map_fn, True)
    # Legge l'input per la parte 2 come lista di stringhe grezze
    data_part_2 = utils.read_input_str(6, str, True)
    # Esegue entrambe le parti
    part_1(data_part_1)
    part_2(data_part_2)