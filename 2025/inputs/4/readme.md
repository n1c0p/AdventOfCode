# Spiegazione dello Script

Questo script risolve un problema che riguarda l'ottimizzazione del lavoro di carrelli elevatori che devono accedere a rotoli di carta rappresentati dal simbolo `@` su una griglia.

## Struttura Generale

Lo script è organizzato in diverse funzioni che collaborano per risolvere due parti del problema:

### Lettura e Preparazione dei Dati

La funzione `map_fn` prepara i dati in ingresso, filtrando solo le righe che contengono i caratteri `@` (rotoli) o `.` (spazi vuoti):

```python
lines = [line.strip() for line in input_file if '@' in line or '.' in line]
```

### Conteggio dei Rotoli Adiacenti

La funzione `count_adjacent_rolls` conta quanti rotoli di carta si trovano nelle 8 posizioni adiacenti a una cella specifica. Utilizza un array di direzioni che rappresenta tutte le posizioni circostanti (diagonali e ortogonali):

```python
directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
```

Per ogni direzione, verifica se la posizione è valida (dentro i limiti della griglia) e se contiene un rotolo `@`.

### Identificazione dei Rotoli Accessibili

La funzione `find_accessible_rolls` attraversa l'intera griglia e identifica quali rotoli possono essere raggiunti dai carrelli. Un rotolo è accessibile se ha **meno di 4 rotoli adiacenti**. Restituisce una lista di coordinate `(row, col)` dei rotoli accessibili.

### Parte 1: Conteggio Iniziale

La funzione `part_1` risolve la prima parte del problema semplicemente contando quanti rotoli sono inizialmente accessibili nella configurazione originale della griglia.

### Parte 2: Rimozione Iterativa

La funzione `remove_accessible_rolls` implementa un processo iterativo:

1. Trova tutti i rotoli accessibili correnti
2. Se non ce ne sono, termina
3. Altrimenti, rimuove questi rotoli (sostituendoli con `.`)
4. Ripete il processo

```python
while True:
    accessible = find_accessible_rolls(grid)
    if not accessible:
        break
    for row, col in accessible:
        grid[row][col] = '.'
    total_removed += len(accessible)
```

Questo simula il processo di rimozione graduale dei rotoli man mano che diventano accessibili, restituendo il numero totale di rotoli rimossi.

### Esecuzione Principale

Il blocco `if __name__ == "__main__"` carica i dati di input ed esegue entrambe le parti del problema. **Nota importante**: `part_2` modifica la griglia originale, quindi se serve mantenere i dati originali, bisognerebbe passare una copia della griglia.