import utils
"""
1. Converto l’intero in stringa.
2. Verifico che abbia lunghezza pari (un numero formato da due copie identiche deve avere lunghezza 2×k).
3. Divido il numero in due metà.
4. Controllo se prima metà == seconda metà.
"""
def is_invalid_id(n: int) -> bool:
    s = str(n)
    # La lunghezza deve essere pari e divisibile in due parti uguali
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    return s[:mid] == s[mid:]

def generate_repeated_ids(max_digits=12):
    """
    Genera tutti gli ID composti da una sequenza ripetuta >=2 volte.
    Esempi validi: 11, 111, 1212, 999, 123123123, ecc.
    """
    invalid = set()

    # Lunghezza totale dell'ID
    for total_len in range(2, max_digits + 1):
        # La sequenza deve essere un divisore della lunghezza totale
        for seq_len in range(1, total_len // 2 + 1):
            if total_len % seq_len != 0:
                continue

            repeats = total_len // seq_len
            if repeats < 2:
                continue

            start = 10**(seq_len - 1)         # senza zeri iniziali
            end = 10**seq_len

            for seq in range(start, end):
                s = str(seq)
                val = int(s * repeats)
                invalid.add(val)

    return invalid

def part_1(ids_input):
    ids = [item.split('-') for item in ids_input[0].split(",")]
    invalid_ids = [id for item in ids for id in range(int(item[0]), int(item[1]) + 1) if is_invalid_id(id)]
    somma_totale = sum(invalid_ids)
    print("Somma id invalidi part_1:", somma_totale)

def part_2(ids_input):
    intervals = [tuple(map(int, item.split("-"))) for item in ids_input[0].split(",")]
    max_val = max(b for _, b in intervals)
    max_digits = len(str(max_val))
    all_invalid = generate_repeated_ids(max_digits)
    res = [id for a, b in intervals for id in all_invalid if a <= id <= b]
    somma_totale = sum(res)
    print("Somma id invalidi part_2:", somma_totale)


if __name__ == "__main__":
    input = utils.read_input(2, str, False)

    #part_1(input)
    part_2(input)