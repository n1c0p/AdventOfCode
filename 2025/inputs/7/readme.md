Questo codice simula il comportamento di raggi di luce/timeline quantistiche attraverso una griglia.

## Funzione `count_beam_splits`

**Scopo**: Conta quante volte un raggio viene diviso attraversando la griglia.

1. **Inizializzazione**: Trova la posizione di partenza `'S'` nella prima riga
2. **Simulazione**: Usa una lista `active_beams` per tracciare tutti i raggi attivi
3. **Movimento**: Ogni iterazione muove i raggi di una riga verso il basso
4. **Gestione splitter `'^'`**: 
   - Quando un raggio incontra uno splitter, incrementa `split_count`
   - Crea due nuovi raggi (sinistra e destra)
5. **Set visited**: Evita di processare più volte la stessa posizione
6. **Terminazione**: I raggi escono quando superano l'ultima riga

## Funzione `count_quantum_timelines`

**Scopo**: Conta il numero totale di timeline quantistiche che escono dalla griglia.

1. **Differenza chiave**: Invece di tracciare singoli raggi, usa un dizionario `current_states` che mappa ogni posizione al numero di timeline che la attraversano
2. **Moltiplicazione**: Quando una timeline incontra uno splitter, il suo conteggio viene duplicato (diviso tra sinistra e destra)
3. **Iterazione per righe**: Processa tutte le timeline riga per riga in modo sincronizzato
4. **Conteggio finale**: Accumula in `'exit'` il numero totale di timeline che escono dal manifold

## Funzione `create_grid`

Estrae la griglia dall'input, iniziando dalla riga contenente `'S'` fino alla fine (escluse linee vuote o separatori `---`).

## Funzioni `part_1` e `part_2`

- **Part 1**: Conta gli split (numero di volte che il raggio si divide)
- **Part 2**: Conta le timeline totali (crescita esponenziale ad ogni split)

## Esempio pratico

Se un raggio incontra 3 splitter in sequenza:
- **Part 1**: Risposta = 3 (numero di split)
- **Part 2**: Risposta = 2³ = 8 (timeline finali)