# Analisi Passo-Passo dello Script

## 1. Importazioni
```python
import utils
from bisect import bisect_right
```
- `utils`: modulo personalizzato per leggere l'input
- `bisect_right`: funzione per ricerca binaria efficiente in liste ordinate

## 2. Funzione `map_ingredient_ids`
```python
def map_ingredient_ids(lines) -> list[tuple[int,int]]:
    return [(int(before), int(after)) for line in lines.split("\n") 
            for before, after in [line.split("-")]]
```
**Scopo**: Converte le stringhe delle gamme in tuple di interi.

**Esempio**:
- Input: `"3-5\n7-9"`
- Output: `[(3, 5), (7, 9)]`

## 3. Funzione `map_fresh_ingredient`
```python
def map_fresh_ingredient(lines) -> list[int]:
    return [int(line) for line in lines.split("\n")]
```
**Scopo**: Converte la lista di ID da stringhe a interi.

**Esempio**:
- Input: `"4\n8\n12"`
- Output: `[4, 8, 12]`

## 4. Funzione `merge_ranges`
```python
def merge_ranges(ranges):
    if not ranges:
        return []
    ranges = sorted(ranges)  # Ordina per start
    merged = [list(ranges[0])]
    
    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end + 1:  # Sovrapposte o adiacenti
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    
    return [(s, e) for s, e in merged]
```
**Scopo**: Ottimizza le gamme unendo quelle sovrapposte/adiacenti.

**Esempio**:
- Input: `[(1, 3), (2, 5), (7, 9)]`
- Output: `[(1, 5), (7, 9)]`

## 5. Funzione `count_fresh_ids`
```python
def count_fresh_ids(ranges, ids):
    merged = merge_ranges(ranges)
    starts = [s for s, _ in merged]  # Solo gli start
    count = 0
    
    for id_val in ids:
        idx = bisect_right(starts, id_val)  # Posizione in lista ordinata
        if idx > 0:
            start, end = merged[idx - 1]
            if start <= id_val <= end:  # Verifica se dentro la gamma
                count += 1
    
    return count
```
**Scopo**: Conta quanti ID cadono dentro le gamme.

**Logica**:
- Usa ricerca binaria per trovare la gamma candidata
- Verifica se l'ID è effettivamente dentro quella gamma

## 6. Funzione `part_1`
```python
def part_1(ingredient_ids, fresh_ingredient):
    result = count_fresh_ids(ingredient_ids, fresh_ingredient)
    print(f"Numero di ID freschi: {result}")
```
**Scopo**: Esegue la parte 1 del problema e stampa il risultato.

## 7. Funzione `part_2`
```python
def part_2(ingredient_ids, fresh_ingredient):
    pass
```
**Scopo**: Placeholder per la parte 2 (non ancora implementata).

## 8. Main
```python
if __name__ == "__main__":
    list_ingredient_ids, list_fresh_ingredient = utils.read_multisection_input(
        5, 
        [map_ingredient_ids, map_fresh_ingredient], 
        False
    )
    part_1(list_ingredient_ids, list_fresh_ingredient)
```
**Flusso**:
1. Legge l'input del giorno 5 usando `utils`
2. Applica le funzioni di mapping alle due sezioni
3. Esegue solo `part_1`

## Complessità Temporale
- `merge_ranges`: O(n log n) per l'ordinamento
- `count_fresh_ids`: O(m log n) dove m = numero ID, n = numero gamme