import heapq
import math
import re
from dataclasses import dataclass
from typing import Counter, Iterable
from scipy.spatial import cKDTree
import utils

class JBox:
    pass

@dataclass(frozen=True)
class JBox:
    """
    Rappresenta una Junction Box (scatola di giunzione) nello spazio 3D.

    Questa classe immutabile memorizza le coordinate tridimensionali di una
    junction box e fornisce metodi per crearla da una stringa e accedere
    alle sue coordinate.

    Attributes:
        x (int): Coordinata X della junction box
        y (int): Coordinata Y della junction box
        z (int): Coordinata Z della junction box

    Note:
        La classe è frozen (immutabile), il che la rende hashable e utilizzabile
        in set e come chiave di dizionari.
    """
    x: int
    y: int
    z: int

    @staticmethod
    def from_string(string: str) -> JBox:
        """
        Crea un'istanza di JBox da una stringa contenente coordinate.

        Estrae tutti i numeri dalla stringa usando un'espressione regolare
        e li utilizza come coordinate x, y, z della junction box.

        Args:
            string (str): Stringa contenente almeno 3 numeri che rappresentano
                         le coordinate (es. "10,20,30" o "x=10 y=20 z=30")

        Returns:
            JBox: Nuova istanza di JBox con le coordinate estratte

        Raises:
            AssertionError: Se la stringa non contiene esattamente 3 numeri
        """
        # Compila un pattern regex per trovare tutti i numeri nella stringa
        pattern = re.compile(r"\d+")
        # Estrae tutti i numeri trovati
        coords = re.findall(pattern, string)
        # Verifica che siano state trovate esattamente 3 coordinate
        assert len(coords) == 3, f"Not enough coordinates from {string=}"
        # Crea e restituisce una nuova istanza JBox convertendo le stringhe in interi
        return JBox(*[int(coord) for coord in coords])

    @property
    def cords(self) -> tuple[int, int, int]:
        """
        Restituisce le coordinate della junction box come tupla.

        Returns:
            tuple[int, int, int]: Tupla contenente le coordinate (x, y, z)
        """
        return self.x, self.y, self.z


def add_new_pair(
        circuits: Counter[frozenset[int]],
        connected: set[int],
        left: int,
        right: int,
) -> None:
    """
    Aggiunge una nuova coppia di nodi ai circuiti esistenti.

    Se uno dei due nodi è già presente in un circuito esistente, la coppia viene
    unita a quel circuito. Altrimenti, viene creato un nuovo circuito contenente
    solo la coppia.

    Args:
        circuits: Counter che mappa circuiti (frozenset di indici) alla loro dimensione
        connected: Set di tutti gli indici di nodi già connessi
        left: Indice del primo nodo della coppia
        right: Indice del secondo nodo della coppia

    Returns:
        None: Modifica circuits e connected in-place
    """
    # Crea un frozenset con i due nodi da connettere
    pair = frozenset([left, right])
    # Aggiunge entrambi i nodi all'insieme dei nodi connessi
    connected.update(pair)

    key_to_delete = None
    # Cerca se uno dei due nodi è già presente in un circuito esistente
    for key in circuits.keys():
        if left in key or right in key:
            # Se trovato, segna il circuito per la rimozione
            key_to_delete = key
            # Crea un nuovo circuito che unisce quello esistente con la nuova coppia
            new_key = frozenset({*key, *pair})
            circuits[new_key] = len(new_key)
    else:
        # Se nessun nodo è presente in circuiti esistenti, crea un nuovo circuito
        connected.update(pair)
        circuits[pair] = 2

    # Rimuove il vecchio circuito se è stato sostituito
    if key_to_delete is not None:
        del circuits[key_to_delete]


def extend_one_circuit(
        circuits: Counter[frozenset[int]],
        present_element: int,
        missing_element: int
) -> None:
    """
    Estende un circuito esistente aggiungendo un nuovo nodo.

    Trova il circuito che contiene present_element e aggiunge missing_element
    a quel circuito, sostituendo il vecchio circuito con uno nuovo più grande.

    Args:
        circuits: Counter che mappa circuiti (frozenset di indici) alla loro dimensione
        present_element: Indice del nodo già presente nel circuito
        missing_element: Indice del nodo da aggiungere al circuito

    Returns:
        None: Modifica circuits in-place
    """
    key_to_delete = None
    for keyset in circuits.keys():
        if present_element in keyset:
            key_to_delete = keyset
            crowd = frozenset({*keyset, missing_element})
            circuits[crowd] = len(crowd)
            break
    del circuits[key_to_delete]


def merge_two_circuits(
        circuits: Counter[frozenset[int]],
        left: int,
        right: int,
) -> None:
    """
    Fonde due circuiti distinti in uno solo.

    Trova i due circuiti che contengono rispettivamente left e right, e li
    unisce in un unico circuito più grande. Se i due nodi sono già nello
    stesso circuito, non fa nulla.

    Args:
        circuits: Counter che mappa circuiti (frozenset di indici) alla loro dimensione
        left: Indice del nodo nel primo circuito
        right: Indice del nodo nel secondo circuito

    Returns:
        None: Modifica circuits in-place. Ritorna None se i nodi sono già nello stesso circuito.
    """
    left_key, right_key = None, None
    for keyset in circuits.keys():
        if left in keyset:
            left_key = keyset
        if right in keyset:
            right_key = keyset
    if left_key == right_key:
        return None
    new_key = frozenset({*left_key, *right_key})
    circuits[new_key] = len(new_key)
    del circuits[left_key]
    del circuits[right_key]
    return None


class PlayGround:
    def __init__(self, lines: list[str]):
        self.neighbors = None
        self.jboxes:list[JBox] = [JBox.from_string(line) for line in lines]

    def find_n_closest_pair_indices(self, number_of_pairs: int) -> Iterable[tuple[int, int]]:
        vectors = [jbox.cords for jbox in self.jboxes]
        max_rank = len(vectors)
        self.neighbors = cKDTree(vectors)

        distances, indices = self.neighbors.query(vectors, k=max_rank+1)
        paired_distance = {}
        for i in range(max_rank):
            for rank in range(1, max_rank+1):
                j = int(indices[i, rank])
                key = (min(i,j), max(i,j))
                distance = distances[i, rank]
                if key not in paired_distance:
                    paired_distance[key] = distance
        return heapq.nsmallest(number_of_pairs, paired_distance.keys(), key=paired_distance.get)


    def circuit_counter(self, connections: int) -> Counter[frozenset[int]]:
        connected: set[int] = set()
        circuits: Counter[frozenset[int]] = Counter()
        for i, j in self.find_n_closest_pair_indices(connections):
            if len(connected) == 0:
                add_new_pair(circuits, connected, i, j)
            elif i not in connected and j not in connected:
                add_new_pair(circuits, connected, i, j)
            elif i in connected and j not in connected:
                extend_one_circuit(circuits, i, j)
                connected.add(j)
            elif i not in connected and j in connected:
                extend_one_circuit(circuits, j, i)
                connected.add(i)
            else:
                merge_two_circuits(circuits, i, j)
        return circuits

    def last_two_junctions_xes(self):
        estimated_connections = math.comb(len(self.jboxes), 2) // 2
        connected: set[int] = set()
        circuits: Counter[frozenset[int]] = Counter()
        for i, j in self.find_n_closest_pair_indices(estimated_connections):
            if len(connected) == 0:
                add_new_pair(circuits, connected, i, j)
            elif i not in connected and j not in connected:
                add_new_pair(circuits, connected, i, j)
            elif i in connected and j not in connected:
                extend_one_circuit(circuits, i, j)
                connected.add(j)
            elif i not in connected and j in connected:
                extend_one_circuit(circuits, j, i)
                connected.add(i)
            else:
                merge_two_circuits(circuits, i, j)
            if len(connected) == len(self.jboxes) and len(circuits.keys()) == 1:
                return self.jboxes[i].x * self.jboxes[j].x
        raise RuntimeError("Raise the estimated_connections")


class Solution:
    def __init__(self):
        self.lines = utils.read_input(8, self.map_fn_str, False)

    def first_task(self, connections=10) -> int:
        playground = PlayGround(self.lines)
        circuits = playground.circuit_counter(connections)
        return math.prod(length for _, length in circuits.most_common(3))


    def second_task(self) -> int:
        playground = PlayGround(self.lines)
        return playground.last_two_junctions_xes()

    @staticmethod
    def map_fn(input_file) -> tuple[int, int, int]:
        x, y, z = map(int, input_file.split(','))
        return x, y, z

    @staticmethod
    def map_fn_str(input_file) -> str:
        return input_file

if __name__ == "__main__":
    solution = Solution()
    print("The first answer is", solution.first_task(10))
    print("The second answer is", solution.second_task())