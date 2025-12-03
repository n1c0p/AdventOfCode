import utils

def map_fn(line):
    return line

def max_shock(line):
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
"""
non funziona correttamente 
"""
# def big_max_shock(line):
#     # trova il valore minimo
#     minimo = min(int(num) for num in line)
#     find_index = line.index(minimo)
#     line.pop(find_index)
#     for item in range(1,4):
#         minimo = min(int(num) for num in line)
#         find_index = line.index(minimo)
#         line.pop(find_index)
#
#     result = ''.join(map(str, line))
#     return int(result)

def best_subsequence_of_length(line, k):
    """
    Restituisce la sottosequenza lessicograficamente massima
    di lunghezza k, mantenendo l'ordine.
    """
    take = k
    n = len(line)
    result = []

    start = 0
    while take > 0:
        # Finestra in cui è possibile scegliere la prossima cifra
        end = n - take

        # Trova la cifra più grande nella finestra line[start : end+1]
        best_digit = max(line[start:end+1])
        pos = line.index(best_digit, start, end + 1)

        result.append(best_digit)
        take -= 1
        start = pos + 1

    return "".join(result)

def total_shock(lines):
    return sum(max_shock(line) for line in lines)

def part_1(data:list[str]) -> None:
    lista = [list(map(int, num)) for item in data for num in item.split()]
    print("Shock totali:", total_shock(lista))

def part_2(data:list[str]):
    total_big_shock = sum(int(best_subsequence_of_length(line, 12)) for line in data)
    print("Big shock totali:", total_big_shock)

if __name__ == "__main__":
    data_input = utils.read_input(3, map_fn, False)
    part_1(data_input)
    part_2(data_input)