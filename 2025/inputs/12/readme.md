Questo script risolve un problema che coinvolge forme (presents) e regioni, verificando quali regioni possono contenere determinate quantità di forme.

## Passo per passo:

### 1. **Parsing dell'input**
```python
*presents, regions = raw_file.split('\n\n')
```
- Divide il file in sezioni separate da righe vuote (`\n\n`)
- Tutte le sezioni tranne l'ultima → `presents` (lista di forme)
- L'ultima sezione → `regions` (elenco di regioni da verificare)

### 2. **Calcolo delle dimensioni delle forme**
```python
shapes = [present.count('#') for present in presents]
```
- Per ogni forma in `presents`, conta quanti caratteri `#` contiene
- Questo rappresenta l'area/dimensione di ciascuna forma

### 3. **Iterazione sulle regioni**
```python
for region in regions.splitlines():
```
- Processa ogni riga della sezione `regions`

### 4. **Parsing di ogni regione**
```python
size, shapes_list = region.split(':')
width, length = map(int, size.split('x'))
quantities = [int(quantity) for quantity in shapes_list.split()]
```
- Divide la riga in due parti: dimensioni (es. `10x20`) e quantità di forme
- Estrae larghezza e lunghezza della regione
- Converte le quantità di forme in una lista di interi

### 5. **Verifica compatibilità**
```python
if sum(shape * quantity for shape, quantity in zip(shapes, quantities)) <= width * length:
    suitable_regions += 1
```
- Calcola l'area totale necessaria: per ogni forma, moltiplica la sua dimensione per la quantità richiesta
- Se l'area totale necessaria ≤ area disponibile (`width * length`), la regione è adatta
- Incrementa il contatore

### 6. **Output**
Stampa il numero totale di regioni adatte.