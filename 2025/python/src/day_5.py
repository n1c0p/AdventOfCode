import utils
from bisect import bisect_right

def map_ingredient_ids(lines) -> list[tuple[int,int]]:
    return [(int(before), int(after)) for line in lines.split("\n") for before, after in [line.split("-")]]

def map_fresh_ingredient(lines) -> list[int]:
    return [int(line) for line in lines.split("\n")]

def merge_ranges(ranges):
    """Unisce le gamme sovrapposte o adiacenti."""
    if not ranges:
        return []

    # Ordina per inizio gamma
    ranges = sorted(ranges)
    merged = [list(ranges[0])]

    for start, end in ranges[1:]:
        last_start, last_end = merged[-1]
        # Se le gamme si sovrappongono o sono adiacenti
        if start <= last_end + 1:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return [(s, e) for s, e in merged]


def count_fresh_ids(ranges, ids):
    """Conta quanti ID sono freschi."""
    merged = merge_ranges(ranges)
    starts = [s for s, _ in merged]
    count = 0

    for id_val in ids:
        # Trova la gamma che potrebbe contenere questo ID
        idx = bisect_right(starts, id_val)
        if idx > 0:
            start, end = merged[idx - 1]
            if start <= id_val <= end:
                count += 1

    return count


def count_total_fresh_ids(ranges):
    """
    Conta il numero totale di ID freschi nei range uniti.
    """
    merged = merge_ranges(ranges)
    total = 0

    for start, end in merged:
        total += end - start + 1  # +1 perché i range sono inclusivi

    return total

def part_1(ingredient_ids:list[tuple[int,int]], fresh_ingredient:list[int]) -> None:
    # Parte 1
    result = count_fresh_ids(ingredient_ids, fresh_ingredient)
    print(f"Numero di ID freschi: {result}")


def part_2(ingredient_ids:list[tuple[int, int]]) -> None:
    result = count_total_fresh_ids(ingredient_ids)
    print(f"Numero di ID freschi: {result}")

if __name__ == "__main__":
    list_ingredient_ids, list_fresh_ingredient = utils.read_multisection_input(5, [map_ingredient_ids, map_fresh_ingredient], False)
    part_1(list_ingredient_ids, list_fresh_ingredient)
    part_2(list_ingredient_ids)
