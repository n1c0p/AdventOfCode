# --- Day 8: Playground ---
Questo script risolve un problema che coinvolge l'analisi di connessioni tra "junction boxes" (scatole di giunzione) in uno spazio 3D.

## Classe `JBox`

```python
@dataclass(frozen=True)
class JBox:
    x: int
    y: int
    z: int
```

- Rappresenta una scatola di giunzione con coordinate 3D
- `frozen=True` la rende immutabile (hashable, utile per i set)
- `from_string()` estrae le coordinate da una stringa usando regex
- `cords` property restituisce una tupla delle coordinate

## Funzioni di Gestione Circuiti

**`add_new_pair()`**
- Aggiunge una nuova coppia di elementi ai circuiti
- Se uno degli elementi appartiene già a un circuito esistente, li fonde
- Altrimenti crea un nuovo circuito con la coppia

**`extend_one_circuit()`**
- Estende un circuito esistente aggiungendo un nuovo elemento
- Trova il circuito contenente `present_element` e aggiunge `missing_element`

**`merge_two_circuits()`**
- Fonde due circuiti quando si crea una connessione tra elementi di circuiti diversi
- Cerca i due circuiti contenenti `left` e `right` e li unisce

## Classe `PlayGround`

**`__init__()`**
- Legge le linee di input e crea una lista di oggetti `JBox`

**`find_n_closest_pair_indices()`**
- Usa `cKDTree` (struttura dati spaziale efficiente) per trovare le coppie di junction boxes più vicine
- Calcola le distanze tra tutti i punti
- Restituisce le N coppie con distanza minima usando `heapq.nsmallest()`

**`circuit_counter()`**
- Costruisce circuiti connettendo progressivamente le coppie più vicine
- Gestisce 4 casi:
  1. Primo circuito (set vuoto)
  2. Entrambi gli elementi non connessi → nuovo circuito
  3. Solo uno connesso → estende il circuito esistente
  4. Entrambi connessi → fonde due circuiti

**`last_two_junctions_xes()`**
- Continua ad aggiungere connessioni fino a quando tutti gli elementi sono in un unico circuito
- Restituisce il prodotto delle coordinate X delle ultime due junction boxes connesse

## Classe `Solution`

**`first_task()`**
- Costruisce i circuiti con un numero limitato di connessioni (default 10)
- Restituisce il prodotto delle lunghezze dei 3 circuiti più grandi

**`second_task()`**
- Trova il momento in cui tutte le junction boxes sono connesse in un unico circuito
- Restituisce il prodotto delle coordinate X delle ultime due connesse

## Logica Generale

Lo script simula la costruzione di una rete di connessioni tra punti 3D, partendo dalle coppie più vicine e unendo progressivamente i circuiti separati fino a formare un'unica rete connessa.