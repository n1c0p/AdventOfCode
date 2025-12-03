import utils

def map_fn(line):
    return line

def max_shock(line:list[int]) -> int:
    """
    Calcola il massimo 'shock' in una riga di cifre.
    Per ogni posizione i prende la cifra in posizione i come decina
    e la cifra massima alla sua destra come unità, formando first*10+second.
    Restituisce il massimo di questi valori.
    """
    best = 0
    # scorri tutte le posizioni per la prima cifra (decina)
    for i in range(len(line) - 1):
        first = int(line[i])
        # trova il valore massimo alla destra di i
        second = max(int(c) for c in line[i + 1:])
        # forma il numero
        shock = first * 10 + second
        # aggiorna se è migliore
        if shock > best:
            best = shock
    return best

def best_subsequence_of_length(line:str, number_to_take:int) -> str:
    """
    Restituisce la sotto sequenza lessicograficamente massima
    di lunghezza number_to_take mantenendo l'ordine originale.
    Algoritmo greedy: per ogni posizione scelta prende la cifra massima
    possibile nella finestra rimanente che consente di completare la
    sotto sequenza della lunghezza richiesta.
    """
    take = number_to_take
    line_length = len(line)
    result = []

    start = 0
    while take > 0:
        # Finestra in cui è possibile scegliere la prossima cifra
        end = line_length - take

        # Trova la cifra più grande nella finestra line[start:end+1]
        best_digit = max(line[start:end+1])
        pos = line.index(best_digit, start, end + 1)

        result.append(best_digit)
        take -= 1
        start = pos + 1

    return "".join(result)

def part_1(data:list[str]) -> None:
    """
    Converte ogni token numerico in una lista di cifre (int) e somma
    i valori max_shock per ogni riga, stampando il totale.
    """
    lista = [list(map(int, num)) for item in data for num in item.split()]
    total_shock = sum(max_shock(line) for line in lista)
    print("Shock totali:", total_shock)

def part_2(data:list[str]) -> None:
    """
    Per ogni riga interpreta la linea come una stringa di cifre e prende
    la sotto sequenza massima di lunghezza 12, la converte in intero e somma.
    """
    total_big_shock = sum(int(best_subsequence_of_length(line, 12)) for line in data)
    print("Big shock totali:", total_big_shock)

if __name__ == "__main__":
    data_input = utils.read_input(3, map_fn, False)
    part_1(data_input)
    part_2(data_input)