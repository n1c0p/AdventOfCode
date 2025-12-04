import utils

def map_fn(input_file):
    lines = [line.strip() for line in input_file if '@' in line or '.' in line]
    return lines

def count_adjacent_rolls(grid, row, col):
    """Conta quanti rotoli di carta sono adiacenti a una posizione"""
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            if grid[new_row][new_col] == '@':
                count += 1

    return count


def find_accessible_rolls(grid):
    """Trova tutti i rotoli accessibili (con meno di 4 adiacenti)"""
    accessible = []

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '@':
                if count_adjacent_rolls(grid, row, col) < 4:
                    accessible.append((row, col))

    return accessible

def remove_accessible_rolls(grid):
    """Rimuove iterativamente i rotoli accessibili"""
    total_removed = 0

    while True:
        # Trova i rotoli accessibili
        accessible = find_accessible_rolls(grid)

        # Se non ci sono rotoli da rimuovere, fermati
        if not accessible:
            break

        # Rimuovi i rotoli accessibili
        for row, col in accessible:
            grid[row][col] = '.'

        total_removed += len(accessible)

    return total_removed

def part_1(data:list[list[str]]) -> None:
    # Parte 1
    accessible = find_accessible_rolls(data)
    print(f"Parte 1: {len(accessible)}")

def part_2(data:list[list[str]]) -> None:
    total = remove_accessible_rolls(data)
    print(f"Parte 2: {total}")

if __name__ == "__main__":
    data_input = utils.read_input(4, map_fn, False)
    part_1(data_input)
    part_2(data_input)