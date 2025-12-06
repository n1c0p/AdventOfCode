import utils

def map_fn(input_file) -> list[list[str]]:
    problems = [line.strip() for line in input_file.split()]
    lines = [line.rstrip() for line in input_file if line.strip()]
    return problems

def part_1(problems: list[list[str]]) -> None:
    list_of_number = problems[:-1]
    list_of_operator = problems[-1]

    results = []
    for i, operator in enumerate(list_of_operator):
        if operator == '+':
            result = sum(int(row[i]) for row in list_of_number)
        else:  # operator == '*'
            result = 1
            for row in list_of_number:
                result *= int(row[i])
        results.append(result)

    print("Result:", sum(results))


def parse_worksheet(lines):
    # Rimuovi righe vuote
    lines = [line.rstrip() for line in lines if line.strip()]

    # Trova la larghezza massima
    max_width = max(len(line) for line in lines)

    # Padding delle righe per avere tutte la stessa lunghezza
    lines = [line.ljust(max_width) for line in lines]

    return lines

def part_2() -> None:
    with open('../../inputs/6/day_6.txt', 'r') as f:
        lines = f.readlines()

    lines = parse_worksheet(lines)
    height = len(lines)
    width = len(lines[0])

    problems = []
    current_problem = []

    # Leggi da destra a sinistra
    for col in range(width - 1, -1, -1):
        column = [lines[row][col] for row in range(height)]

        # Se la colonna è vuota, separa i problemi
        if all(c == ' ' for c in column):
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(column)

    if current_problem:
        problems.append(current_problem)

    total = 0
    for problem in problems:
        operator = problem[-1][-1]
        numbers = []
        for col in problem:
            num_str = ''.join(col).strip()
            if num_str:
                app = num_str.replace('+', '').replace('*', '')
                numbers.append(int(app))

        result = numbers[0]
        for num in numbers[1:]:
            if operator == '+':
                result += num
            elif operator == '*':
                result *= num

        total += result

    print("Result part 2:", total)


if __name__ == "__main__":
    data_input = utils.read_input(6, map_fn, True)
    data_input2 = utils.read_input(6, str, True)
    #part_1(data_input)
    part_2()
