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


def generate_repeated_ids(max_digits: int = 12) -> set[int]:
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
            start = 10 ** (seq_len - 1)  # senza zeri iniziali
            end = 10 ** seq_len

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


def part_1(ids_input) -> None:
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


def part_2(ids_input) -> None:
    """
    Tramite list comprehension genero la lista di tuple (a, b) dagli intervalli forniti in input.

        - ids_input[0] è una stringa che contiene intervalli separati da virgole, es: "10-50,100-200".
        - split(",") divide la stringa in pezzi: ["10-50", "100-200"]
        - Ogni pezzo viene poi suddiviso con split("-") → ["10", "50"]
        - map(int, ...) converto le due parti in numeri
        - tuple(...) li mette in una tupla (a, b)

    Risultato:
    intervals = [(10, 50), (100, 200)] (esempio)
    """
    intervals = [tuple(map(int, item.split("-"))) for item in ids_input[0].split(",")]

    """
    Trovo il valore massimo tra le estremità degli intervalli
    
        - Estrae tutti i valori b dalle tuple (a, b)
        - Calcola il massimo
        
    Es: da [(10,50),(100,200)] ottiene max_val = 200.
    """
    max_val = max(b for _, b in intervals)

    """ 
    Calcolo il numero di cifre del valore massimo 
    
    Se max_val = 200 → str(200) = "200" → len(...) = 3
 🔎 Serve per generare numeri fino a quella lunghezza (1 cifra, 2 cifre, 3 cifre, ecc.)
    """
    max_digits = len(str(max_val))

    """
    Genero tutti i numeri ripetuti fino al numero di cifre massimo richiesto
    Es. con n = 3 potrebbe generare 11, 22, 33, ..., 111, 222, 333, ...
    """
    all_invalid = generate_repeated_ids(max_digits)

    """
    Seleziono solo quelli che ricadono negli intervalli forniti e tramite una list comprehension li metto in una lista.
    Questa è una list comprehension doppia:
    Per ogni intervallo (a, b) e per ogni numero id nella lista di numeri “ripetuti”, prendo solo gli id che sono compresi tra a <= id <= b.

🔎  Risultato: una lista di invalid IDs che cadono nei range.
    """
    res = [id for a, b in intervals for id in all_invalid if a <= id <= b]

    """
    Calcolo la somma totale degli ID invalidi trovati e la stampo.
    """
    somma_totale = sum(res)
    print("Somma id invalidi part_2:", somma_totale)


if __name__ == "__main__":
    input = utils.read_input(2, str, False)
    part_1(input)
    part_2(input)