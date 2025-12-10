Lo script risolve un problema che coinvolge coordinate 2D e calcolo di aree di rettangoli.

## Funzioni di utilità

**`map_fn(input_file)`**: Converte una riga di input in formato `"x,y"` in una tupla di interi `(x, y)`.

**`pairs(tiles, size)`**: Data una lista di coordinate, restituisce coppie consecutive di punti, dove l'ultima coppia collega l'ultimo punto al primo (struttura circolare).

## Parte 1 - Area massima senza vincoli

**`largest(tiles)`**: Calcola l'area del rettangolo più grande che può essere formato da due punti qualsiasi della lista. Per ogni coppia di punti:
- Calcola la distanza Manhattan incrementata di 1 per ogni dimensione
- Moltiplica larghezza × altezza per ottenere l'area
- Tiene traccia dell'area massima trovata

**`part_1(tiles)`**: Esegue `largest()` e stampa il risultato.

## Parte 2 - Area massima evitando i bordi

**`edges`** (in `part_2`): Crea una lista di rettangoli (bordi) definiti da ogni coppia consecutiva di punti. Ogni bordo è rappresentato come `(x_min, y_min, x_max, y_max)`.

**`intersect(edges, x1, y1, x2, y2)`**: Verifica se un rettangolo `(x1,y1)-(x2,y2)` interseca uno qualsiasi dei bordi. Usa il controllo classico di sovrapposizione di rettangoli.

**`largest_inside(edges, tiles)`**: Come `largest()`, ma accetta solo rettangoli che **non intersecano** i bordi definiti. Per ogni coppia di punti:
- Calcola il rettangolo normalizzato (coordinate minime e massime)
- Verifica che non intersechi i bordi
- Tiene traccia dell'area massima valida

**`part_2(tiles)`**: Costruisce i bordi e trova l'area massima che li evita.

## Esecuzione principale

Legge i dati dal file di input (giorno 9) ed esegue entrambe le parti del problema.