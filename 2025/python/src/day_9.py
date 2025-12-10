import utils
"""
Converte una stringa nel formato "x,y" in una tupla di interi (x, y)
"""
def map_fn(input_file) -> tuple[int, int]:
    x, y = map(int, input_file.split(','))
    return x, y

"""
Crea coppie consecutive di elementi dalla lista (ultimo elemento si collega al primo)
Utile per rappresentare i bordi di un poligono chiuso
"""
def pairs(tiles: list[tuple[int,int]], size:int) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    return [(tiles[i], tiles[(i+1) % size]) for i in range(size)]

"""
Calcola l'area massima del rettangolo tra due punti qualsiasi della lista
Aggiunge 1 alle dimensioni (probabilmente per inclusione dei bordi)
"""
def largest(tiles: list[tuple[int,int]]) -> int:
    best = 0
    for n, xy1 in enumerate(tiles[:-1]):
        for xy2 in tiles[n + 1:]:
            best = max(best, (abs(xy1[0] - xy2[0]) + 1) * (abs(xy1[1] - xy2[1]) + 1))
    return best

"""
Verifica se un rettangolo definito da (x1,y1,x2,y2) interseca uno dei bordi/edge forniti
"""
def intersect(edges: list[tuple[int, int, int, int]], x1:int, y1:int, x2:int, y2:int) -> bool:
    for edge in edges:
        if x1 < edge[2] and x2 > edge[0] and y1 < edge[3] and y2 > edge[1]:
            return True
    return False

"""
Trova l'area massima di un rettangolo tra due punti che NON interseca nessun bordo
"""
def largest_inside(edges: list[tuple[int, int, int, int]], tiles: list[tuple[int,int]]) -> int:
    best = 0
    for n, xy1 in enumerate(tiles[:-1]):
        for xy2 in tiles[n + 1:]:
            x1, x2 = (xy1[0], xy2[0]) if xy1[0] < xy2[0] else (xy2[0], xy1[0])
            y1, y2 = (xy1[1], xy2[1]) if xy1[1] < xy2[1] else (xy2[1], xy1[1])
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            if area > best and not intersect(edges, x1, y1, x2, y2):
                best = area
    return best

"""
Parte 1: trova l'area massima tra due punti qualsiasi
"""
def part_1(tiles: list[tuple[int,int]]) -> None:
    result = largest(tiles)
    print(f"Result part 1", result)

"""
Parte 2: crea i bordi del poligono, quindi trova l'area massima che non li interseca
"""
def part_2(tiles: list[tuple[int,int]]) -> None:
    size = len(tiles)
    edges: list[tuple[int, int, int, int]] = [((xy1[0] if xy1[0] < xy2[0] else xy2[0]),
                                               (xy1[1] if xy1[1] < xy2[1] else xy2[1]),
                                               (xy2[0] if xy1[0] < xy2[0] else xy1[0]),
                                               (xy2[1] if xy1[1] < xy2[1] else xy1[1]))
                                              for xy1, xy2 in pairs(tiles, size)]

    result = largest_inside(edges, tiles)
    print(f"Result part 2", result)

if __name__ == "__main__":
    data = utils.read_input(9, map_fn, False)
    # Esegue entrambe le parti
    part_1(data)
    part_2(data)