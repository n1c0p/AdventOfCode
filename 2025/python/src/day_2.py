import utils
"""
1. Converto l’intero in stringa.
2. Verifico che abbia lunghezza pari (un numero formato da due copie identiche deve avere lunghezza 2×k).
3. Divido il numero in due metà.
4. Controllo se prima metà == seconda metà.

Controlla se un intero `n` è formato da due metà identiche.
Nota: questa funzione verifica solo la condizione "abbastanza semplice"
di due metà identiche (es.: 1212 -> True), non tutte le ripetizioni
(es.: 111 è una ripetizione di '1' tre volte ma qui non verrebbe catturata).
"""
def is_invalid_id(n: int) -> bool:
    s = str(n)
    # La lunghezza deve essere pari e divisibile in due parti uguali
    if len(s) % 2 != 0:
        return False
    mid = len(s) // 2
    # Restituisce True se la prima metà è uguale alla seconda
    return s[:mid] == s[mid:]
"""
Genera tutti gli interi che sono ottenuti ripetendo una sequenza
di cifre almeno 2 volte (es.: 11, 1212, 123123).
max_digits: lunghezza massima totale dell'ID da considerare.
"""
def generate_repeated_ids(max_digits=12):
    """
    Genera tutti gli ID composti da una sequenza ripetuta >=2 volte.
    Esempi validi: 11, 111, 1212, 999, 123123123, ecc.
    """
    invalid = set()

    # Scorro tutte le lunghezze totali possibili dagli 2 fino a max_digits
    for total_len in range(2, max_digits + 1):
        # seq_len è la lunghezza della sequenza ripetuta
        # deve essere un divisore della lunghezza totale e permettere >=2 ripetizioni
        for seq_len in range(1, total_len // 2 + 1):
            if total_len % seq_len != 0:
                continue

            repeats = total_len // seq_len
            if repeats < 2:
                continue

            # Evito sequenze con zeri iniziali: la prima cifra deve essere diversa da zero
            start = 10**(seq_len - 1)         # senza zeri iniziali
            end = 10**seq_len

            # Per ogni possibile sequenza di lunghezza seq_len genero il valore ripetuto
            for seq in range(start, end):
                s = str(seq)
                val = int(s * repeats)
                invalid.add(val)

    return invalid

"""
PARTE 1:
ids_input: lista con la prima riga dell'input (es.: "100-200,300-400")
Per ogni intervallo genera gli ID e somma quelli che soddisfano is_invalid_id.
"""
def part_1(ids_input):
    ids = [item.split('-') for item in ids_input[0].split(",")]
    # Lista di ID considerati "invalidi" secondo is_invalid_id
    invalid_ids = [id for item in ids for id in range(int(item[0]), int(item[1]) + 1) if is_invalid_id(id)]
    somma_totale = sum(invalid_ids)
    print("Somma id invalidi part_1:", somma_totale)

"""
PARTE 2:
Calcola la somma degli ID invalidi usando l'insieme generato da generate_repeated_ids.
Questo approccio è più efficiente quando gli intervalli sono ampi perché si filtra
solo l'insieme già noto di numeri ripetuti.
"""
def part_2(ids_input):
    intervals = [tuple(map(int, item.split("-"))) for item in ids_input[0].split(",")]
    max_val = max(b for _, b in intervals)
    max_digits = len(str(max_val))
    # Genero tutti i numeri ripetuti fino al numero di cifre massimo richiesto
    all_invalid = generate_repeated_ids(max_digits)
    # Seleziono solo quelli che ricadono negli intervalli forniti
    res = [id for a, b in intervals for id in all_invalid if a <= id <= b]
    somma_totale = sum(res)
    print("Somma id invalidi part_2:", somma_totale)


if __name__ == "__main__":
    # Legge l'input usando la funzione helper del progetto
    input = utils.read_input(2, str, False)
    part_1(input)
    part_2(input)