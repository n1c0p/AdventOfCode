# Analisi del Problema
Questo è un problema di algebra lineare su GF(2) (campo di Galois con 2 elementi). Ogni bottone può essere premuto 0 o più volte, e premere un bottone un numero pari di volte equivale a non premerlo (dato che ogni luce viene toggleata).
Il problema si riduce a trovare il minimo numero di bottoni da premere un numero dispari di volte per ottenere la configurazione target.

# Spiegazione del Codice

Questo codice risolve un puzzle che coinvolge macchine con bottoni e luci/voltaggio. Il problema viene affrontato in due modi diversi per due parti del puzzle.

## Struttura dei Dati

La classe `MachineConfiguration` rappresenta una macchina e prepara i dati per la risoluzione tramite programmazione lineare. Nel costruttore, i bottoni vengono convertiti in rappresentazioni binarie:

```python
binary_toggle = [int(i in toggle) for i, _ in enumerate(self.joltages)]
```

Questo crea un array dove ogni posizione indica se il bottone influenza quella specifica posizione (1) o no (0). I bottoni vengono poi ordinati in base al numero di posizioni che influenzano.

## Parsing dell'Input

La funzione `map_fn` suddivide ogni riga di input in tre componenti sostituendo i separatori e dividendo la stringa. La funzione `parse_machine` estrae i dati strutturati usando espressioni regolari:

```python
target = [1 if item == '#' else 0 for item in target_match.group(1)]
```

Questo converte il diagramma delle luci in una lista binaria, dove `#` rappresenta una luce accesa (1) e `.` una luce spenta (0).

## Parte 1: Approccio a Forza Bruta

La funzione `solve_machine` utilizza un approccio di forza bruta per trovare la soluzione minima. Prova tutte le combinazioni possibili di bottoni, partendo da zero bottoni fino al massimo disponibile:

```python
for combo in combinations(range(len(buttons)), n_buttons):
    state = [0] * n_lights
    for button_idx in combo:
        for light_idx in buttons[button_idx]:
            state[light_idx] ^= 1
```

L'operatore XOR (`^= 1`) inverte lo stato della luce: se era 0 diventa 1 e viceversa. Quando lo stato raggiunto corrisponde al target, restituisce il numero di bottoni premuti.

## Parte 2: Programmazione Lineare

Il metodo `solve_with_linear_solver` utilizza OR-Tools per risolvere il problema come un problema di ottimizzazione lineare intera. Crea variabili che rappresentano quante volte ogni bottone viene premuto:

```python
x = [solver.IntVar(0, solver.infinity(), f"x_{k}") for k in range(number_of_variables)]
```

Per ogni posizione di voltaggio, aggiunge un vincolo che garantisce che la somma degli effetti di tutti i bottoni sia uguale al voltaggio target:

```python
solver.Add(sum(self.toggles[k][j] * x[k] for k in range(number_of_variables)) == self.joltages[j])
```

L'obiettivo è minimizzare il numero totale di pressioni: `solver.Minimize(solver.Sum(x))`.

Questo approccio è più efficiente del brute force quando il numero di variabili è elevato o quando i bottoni possono essere premuti più volte.