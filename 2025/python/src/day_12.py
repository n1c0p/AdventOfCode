import utils

def part_1(raw_file: str):
    """
    La funzione `split('\n\n')` divide il contenuto del file in base a doppie interruzioni di riga (due newline consecutive).

    Come funziona in questo contesto:

    1. `f.read()` legge l'intero contenuto del file come stringa
    2. `split('\n\n')` divide la stringa in una lista usando `\n\n` come separatore
    3. `*presents, regions` usa l'unpacking per assegnare:
       - Tutti gli elementi tranne l'ultimo alla lista `presents` (grazie all'operatore `*`)
       - L'ultimo elemento alla variabile `regions`

    Questo pattern è utile quando il file ha più sezioni separate da righe vuote e vuoi trattare l'ultima sezione diversamente dalle precedenti.
    """
    *presents, regions = raw_file.split('\n\n')

    shapes = [present.count('#') for present in presents]
    suitable_regions = 0
    for region in regions.splitlines():
        size, shapes_list = region.split(':')
        width, length = map(int, size.split('x'))
        quantities = [int(quantity) for quantity in shapes_list.split()]
        total_area_required = sum(shape * quantity for shape, quantity in zip(shapes, quantities))
        available_area = width * length
        if total_area_required <= available_area:
            suitable_regions += 1

    print(f"Result {suitable_regions}")

if __name__ == "__main__":
    data = utils.read_input_entire_str(12, True)
    part_1(data)

