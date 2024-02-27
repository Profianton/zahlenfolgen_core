from .rechner.math_eval import calculate as calc
from time import time
import os
from matplotlib import pyplot as plt
from fractions import Fraction
plt.switch_backend('agg')                    # stabilisiert Plots

# zahl schön darstellen


def stringify_number(number):
    fraction = Fraction(number).limit_denominator()
    whole_part = int(fraction)
    fractional_part = fraction - whole_part
    if fractional_part == 0:
        return str(whole_part)
    elif whole_part == 0:
        return str(fractional_part)
    else:
        return f"{whole_part}+{fractional_part}"

# Überprüfen, ob eine nicht rekursive folge die richtige ist


def check_expression(string):
    for idx, num in enumerate(list_with_numbers):
        if calculate(idx + 1, string) != num:  # Wenn eine Folge nicht passt, gebe None zurück
            return None
    # Rechne nächstes Element aus, wenn die ersten Folgeglieder passen
    n = len(list_with_numbers) + 1
    result = calculate(n, string)
    if result != None:
        return string, result, "Normal"

# Einen Operator und eine Zahl Ergänzen, wenn Komplexitat übrig ist, sonst Formel prüfen
# Die Komplexität wird erhöht, wenn ein Operator, wie +, -, *, /, ^ eingefügt wird.


def normal_move(complexity_left, string):
    if complexity_left == 0:
        # Formel prüfen
        return check_expression(string)
    # operator anhängen
    for operator in operators:
        if operator["c"] <= complexity_left:
            # Zahl anhängen
            for num in numbers:
                result = normal_move(
                    complexity_left -
                    operator["c"], string + operator["z"] + num
                )
                # Ergebnis der Formel zurückgeben, wenn die Formel passt
                if result != None:
                    return result

# Funktion zum Ausrechnen von nicht-rekursiven Formeln


def calculate(n, string):
    string = string.replace("n", str(n))
    try:
        return calc(string)
    except ZeroDivisionError:
        return None

# Negative Zahlen für calc vorbereiten


def tokenize_fix(num):
    if num < 0:
        return f"(0-{-num})"
    else:
        return str(num)

# Funktion zum Ausrechnen von rekursiven Formeln


def calculate_recursive(n, string):
    # Elemente f(n-1) und f(n-2) durch den Wert ersetzen und n einfügen
    string = (
        string.replace("f(n-2)", tokenize_fix(list_with_numbers[n - 3]))
        .replace("f(n-1)", tokenize_fix(list_with_numbers[n - 2]))
        .replace("n", str(n))
    )
    try:
        # ausrechnen
        return calc(string)
    except ZeroDivisionError:
        return None

# Einen Operator und eine Zahl ergänzen, solange Komplexität übrig ist, ansonsten Formel prüfen für nicht-rekursive Folgen
# Die Komplexität wird erhöht, wenn ein Operator, wie +, -, *, /, ^ eingefügt wird.


def recursive_normal_move(complexity_left, string):
    if complexity_left == 0:
        if not (("f(n-2)" in string) or ("f(n-1)" in string)):
            return None
        items_to_check = list(enumerate(list_with_numbers))
        if "f(n-2)" in string:
            items_to_check = items_to_check[2:]
        else:
            items_to_check = items_to_check[1:]
        for idx, num in items_to_check:
            if calculate_recursive(idx + 1, string) == num:
                1
            else:
                return None
        i = len(list_with_numbers) + 1
        result = calculate_recursive(i, string)
        if result != None:
            return string, result, "Recursive"
        else:
            return None
    for operator in operators:
        if operator["c"] <= complexity_left:
            for num in numbers_recusive:
                result = recursive_normal_move(
                    complexity_left -
                    operator["c"], string + operator["z"] + num
                )
                if result != None:
                    return result


def recusive_first_move(complexity):
    global numbers_recusive
    numbers_recusive = numbers + ["f(n-1)", "f(n-2)", "(f(n-1)-f(n-2))"]
    for number in numbers_recusive:
        result = recursive_normal_move(complexity, number)
        if result != None:
            return result


def first_move(complexity):
    for num in numbers:
        result = normal_move(complexity, num)
        if result != None:
            return result
    if complexity - 1 >= 0:
        return recusive_first_move(complexity - 1)


def run_with_complexity(max_complexity):
    global operators, numbers
    operators = [
        {"z": "*", "c": 1},
        {"z": "/", "c": 1},
        {"z": "+", "c": 1},
        {"z": "-", "c": 1},
        {"z": "^", "c": 1},
    ]
    numbers = [f"{num}" for num in list(range(0, 6))] + ["n", "(n-1)", "(0-1)"]

    return first_move(max_complexity)


def get_inputs():
    list_with_numbers = []
    os.system("cls" if os.name == "nt" else "clear")
    while True:
        if list_with_numbers == []:
            string = f"Enter a number:"
        else:
            string = f"Enter a number (or press 'Enter' to finish)\n {', '.join(
                [stringify_number(number) for number in list_with_numbers])}, "
        number = input(string)
        os.system("cls" if os.name == "nt" else "clear")
        if number == "" and list_with_numbers != []:
            break
        else:
            try:
                number = eval(number)
                if type(number) == float or type(number) == int:
                    list_with_numbers.append(number)
            except:
                print("Invalid input")
    print(
        f"\nYou entered the following numbers: {
            ', '.join([stringify_number(number) for number in list_with_numbers])}"
    )
    return list_with_numbers


real_print = print


def solve(numbers):
    global log
    log = ""
    # custom print Funktion, um alles mit zu loggen

    def print(x):
        global real_print
        real_print(x)
        global log
        log += str(x) + "\\n"

    print(f"solving {numbers}")
    global list_with_numbers
    list_with_numbers = numbers
    global complexity
    complexity = 0
    solved = False
    start_time = time()
    while not solved:
        print(f"Running with complexity {complexity}.")
        complexity_start_time = time()
        output = run_with_complexity(complexity)
        print(
            f"complexity {complexity} finished in {
                round(time()-complexity_start_time, 5)} seconds."
        )
        if output != None:
            formula, next_number, type = output
            for i in range(len(list_with_numbers) + 1, len(list_with_numbers) + 10):
                list_with_numbers.append(calculate_recursive(i, formula))

            if type == "Normal":
                print(
                    f"the formula was '{formula}' and the next numbers are {', '.join([stringify_number(
                        calculate(i, formula)) for i in range(len(list_with_numbers)+1, len(list_with_numbers)+5)])}."
                )
                # list_with_numbers+=[calculate(i,formula) for i in range(len(list_with_numbers)+1,len(list_with_numbers)+5)]
                # [calculate(i,formula) for i in range(0,len(list_with_numbers)+10,0.1)]
                plt.plot(
                    [i /
                        10 for i in range(0, (len(list_with_numbers) + 10) * 10, 1)],
                    [
                        calculate(i / 10, formula)
                        for i in range(0, (len(list_with_numbers) + 10) * 10, 1)
                    ],
                )
                plt.plot(

                    [
                        calculate(i, formula)
                        for i in range(0, (len(list_with_numbers) + 10), 1)
                    ],
                    "o "
                )
            else:
                ols_list_with_numbers = list_with_numbers.copy()
                for i in range(len(list_with_numbers) + 1, len(list_with_numbers) + 10):
                    list_with_numbers.append(calculate_recursive(i, formula))
                plt.plot(
                    list_with_numbers,
                    "o-"
                )
                print(
                    f"the recursive formula was 'f(n)={formula}' and the next numbers are {', '.join(
                        [stringify_number(number) for number in list_with_numbers[len(ols_list_with_numbers):]])}."
                )

            print(
                f"solved complexity {complexity} problem in {
                    round(time()-start_time, 5)} seconds."
            )
            # plot generieren
            plt.clf()
            plt.xticks(range(0, len(list_with_numbers), 1))
            plt.title("Folge")

            plt.savefig(f"{zahlenfolgen_dir}/plot.png")
            plt.clf()
            plt.xticks(range(0, len(list_with_numbers), 1))

            plt.title("Reihe (Summe der Folgenelemente)")
            series = [sum(list_with_numbers[:i+1]) for i in range(
                0, len(list_with_numbers), 1)]  # Mathematische Reihe
            plt.plot(
                series,
                "o-"
            )

            plt.savefig(f"{zahlenfolgen_dir}/series.png")

            solved = True
            print((formula, list_with_numbers, type))
            return (formula, list_with_numbers, type, log, series)
        else:
            complexity += 1


if __name__ == "__main__":
    start = time()
    for _ in range(5):
        solve([1, 1, 2, 3, 5, 8, 13])
    print(f"time_average: {(time()-start)/5}")
zahlenfolgen_dir = "/".join(__file__.replace("\\", "/").split("/")[:-2])
