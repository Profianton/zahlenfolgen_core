import math


'''In math_eval wird eine eigene Funktion geschrieben, die die  Standard-Auswerte-Funktion eval ersetzen kann'''


class operator:
    """Klasse in der alle Operatoren zum Ausrechnen gespeichert sind. D.h. aus dem Rechenzeichen wird eine Funktion"""

    def __init__(self, zeichen, name, function):
        self.zeichen, self.name, self.function = zeichen, name, function

    def __repr__(self):
        return f"operator({self.name})"


class nested_value:
    pass


class nested_operator(nested_value):
    def __init__(self, op: operator, a: nested_value, b: nested_value) -> None:
        self.op: operator = op
        self.a: nested_value = a
        self.b: nested_value = b

    def __float__(self):
        return self.op.function(float(self.a), float(self.b))


class number(nested_value):
    def __init__(self, val: float) -> None:
        self.val: float = val

    def __float__(self):
        return self.val

    def __repr__(self) -> str:
        return str(self.val)


class klammer:
    def __init__(self, dir):
        self.dir = dir


def add(x: float, y: float):
    """Addiere zwei Zahlenwerte 

    Args:
        x (int | float ): 1.Summand
        y (int | float ): 2.Summand
    Returns:
        int | float : Summe
    """
    return x + y


def subtract(x, y):
    """Subtrahiere zwei Zahlenwerte

    Args:
        x (int | float ): Minuend
        y (int | float ): Subtrahend

    Returns:
        (int | float ) : Differenz
    """
    return x - y


def divide(x, y):
    """Dividiere zwei Zahlenwerte

    Args:
        x (int | float ): Dividend
        y (int | float ): Divisor

    Returns:
        int | float : Quotient
    """
    return x / y


def multiply(x, y):
    """Multipliziere zwei Zahlenwerte

    Args:
        x (int | float ): 1.Faktor
        y (int | float ): 2.Faktor

    Returns:
        int | float : Produkt
    """
    return x * y


def pow(b, e):
    """Potenzen berechnen; 
    Abbruch, wenn die Zahl zu groß wird
    In meiner Anwendung steht im Exponenten kein float, prinzipiell wäre das aber möglich.

    Args:
        b (int | float ): Basis
        e (int | float ): Exponent

    Returns:
         int | float : Ergebnis der Potenzaufgabe
    """
    try:
        return b**e
    except:
        return math.inf


operators = [
    # definiere Malzeichen als Funktion multiply
    operator("*", "o_mal", multiply),
    # definiere Geteiltzeichen als Funktion divide
    operator("/", "o_teilen", divide),
    # definiere Pluszeichen als Funktion add
    operator("+", "o_plus", add),
    # definiere Minuszeichen als Funktion subtract
    operator("-", "o_minus", subtract),
    # definiere Potenzzeichen als Funktion pow
    operator("^", "o_power", pow),
]


def is_operator(char):
    """Überprüft ob ein beliebiges Zeichen ein Rechenzeichen (Teil der Liste operators) ist.

    Args:
        char (string): Beliebiges Zeichen

    Returns:
        bool: Ja, wenn Zeichen in der Liste operators ist. Nein, wenn es nicht in der Liste operators ist.
    """
    return operators_dict.get(char, False) != False


operators_dict = {e.zeichen: e for e in operators}


def get_operator_from_string(string):
    """Es wird der passende Rechenoperator inkl. Funktion passend zum Rechenzeichen zurückgegeben

    Args:
        string (string): ein Rechenzeichen

    Returns:
        operator: Gibt einen Rechenoperator zurück.
    """
    return operators_dict[string]


def analyse(string):
    """Hier wird die Formel analysiert und tokenized (Mit Tokenizing kann ein String in Tokens aufgeteilt werden.)

    Args:
        string (string): Formel

    Raises:
        ValueError: Keine sinnvolle Formel

    Returns:
        list: Tokenisierter string
    """
    string = string.replace(",", ".")
    parts = []
    i = 0

    nums = [str(num) for num in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]] + ["."]
    while i < len(string):
        char = string[i]
        if char in nums:
            num = ""
            while char in nums:
                num += char
                i += 1
                if i >= len(string):
                    break
                char = string[i]

            parts.append(number(float(num)))
            continue
        elif is_operator(char):
            parts.append(get_operator_from_string(char))
        elif char in ["(", ")"]:
            if char == "(":
                parts.append(klammer(1))
            else:
                parts.append(klammer(-1))
        else:
            raise ValueError(
                f"non-valid character:{char} in string:{string} at position {i}"
            )
        i += 1
    return parts


# Hier wird die Reihenfolge festgelegt, so dass auch der Computer nach den allgemeinen Rechengesetzen arbeitet.
# Klammer vor Potenz, vor Punkt (* und geteilt), vor Strich
reihenfolge = [
    [get_operator_from_string("^")],
    [get_operator_from_string("*"), get_operator_from_string("/")],
    [get_operator_from_string("+"), get_operator_from_string("-")],
]


def parse_to_nested_operator(parts):
    """Diese Funktion verwandelt eine liste von Operatoren in eine baumstruktur

    Args:
        parts: liste von Operatoren und Zahlen

    Returns:
        nested_value
    """
    for operators_on_level in reihenfolge:
        i = 0
        while i < len(parts):
            value = parts[i]
            if type(value) == operator:
                if value in operators_on_level:
                    parts[i-1:i+1] = nested_operator(
                        value, parts[i - 1], parts[i + 1]),

                    # parts.pop(i - 1)
                    i -= 1
                    # parts.pop(i + 1)
                    continue

            i += 1

    return parts[0]


def parse_klammern(parts):
    """Hauptfunktion um den String zu parsen
        Priorisierung von Klammern in Rechenausdrücken

    Args:
        parts (list): tokenised String

    Returns:
        parsed Formel
    """
    i = 0
    klammer_layer = 0
    while i < len(parts):
        value = parts[i]
        if type(value) == klammer:
            if value.dir == 1:
                klammer_layer += 1
                if klammer_layer == 1:
                    start_i = i
            else:
                klammer_layer -= 1

                if klammer_layer == 0:
                    parts[start_i: i +
                          1] = [parse_klammern(parts[start_i + 1: i])]
                    i = start_i

        i += 1

    parts = parse_to_nested_operator(parts)

    return parts

# fix


def get_title(node):
    """Funktion, die den Namen eines Elements im Rechenbaums generiert - wird zum Debuggen verwendet"""
    type_of_node, value = node
    if type_of_node == "n":
        return value
    elif type_of_node == "o":
        return value.zeichen
    elif type_of_node == "no":
        return value["o"].zeichen
    else:
        raise ValueError("node not known   node:" + node)

# fix


def draw_node(node):
    """Funktion, zum Zeichnen eines Rechenbaums - wird hauptsächlich zum Debuggen von math_eval verwendet"""
    type_of_node, value = node
    result = calculate_from_node(node)
    string = (
        f""" _______
/       \\
| (={str(result)}){" "*(3-len(str(result)))}|
| {get_title(node)}{" "*(6-len(str(get_title(node))))}|
\\_______/"""
        + "\n"
    )
    if type_of_node == "no":
        left_node_string = draw_node(value["other_points"][0])
        right_node_string = draw_node(value["other_points"][1])
        left_node_string = "\n".join(
            left_node_string.splitlines()
            + (
                [" " * len(left_node_string.splitlines()[0])]
                * (
                    max(
                        [
                            len(left_node_string.splitlines()),
                            len(right_node_string.splitlines()),
                        ]
                    )
                    - len(left_node_string.splitlines())
                )
            )
        )

        right_node_string = "\n".join(
            right_node_string.splitlines()
            + (
                [" " * len(left_node_string.splitlines()[0])]
                * (
                    len(left_node_string.splitlines())
                    - len(right_node_string.splitlines())
                )
            )
        )

        string = "\n".join(
            [
                " " *
                (math.ceil(len(left_node_string.splitlines()[0]) / 2) * 2 + 1)
                + line
                for line in string.splitlines()
            ]
            + [""]
        )
        string += (
            " " * (math.ceil(len(left_node_string.splitlines()[0]) / 2 + 1))
            + "_" * (math.ceil(len(left_node_string.splitlines()[0]) / 2 + 2))
            + "/  \\"
            + "_" * (math.ceil(len(right_node_string.splitlines()[0]) / 2 + 2))
        )
        string += "".join(
            [
                "\n  " + left + " " * 8 + right
                for left, right in zip(
                    left_node_string.splitlines(), right_node_string.splitlines()
                )
            ]
        )
    length = max([len(line) for line in string.splitlines()])
    string = "\n".join(
        [line + " " * (length - len(line)) for line in string.splitlines()]
    )
    return string


def parse(string, should_draw_node=False):
    """Wrapper für parse-Klammern - vereinfacht das Parsen

    Args:
        string (string): Formel
        should_draw_node (bool, optional): Rechenbaum generieren. Defaults to False.

    Returns:
        parsed Formel
    """

    parts = analyse(string)
    node = parse_klammern(parts)
    if should_draw_node:
        with open("node", "w", encoding="UTF-8") as f:
            f.write(draw_node(node))
    return node


def calculate(string):
    """Wrapper für das Ausrechnen - vereinfacht das Ausrechnen

    Args:
        string (string): Formel

    Returns:
        int | float: Ergebnis
    """
    return calculate_from_node(parse(string))


def calculate_from_node(node) -> int | float:
    """Ausrechnen der Zahlenwerte über die geparsten Formeln
    erwartet als Eingabe den geparsten String mit der Rechenvorschrift

    Args:
        node: geparster Teil des Rechenbaums

    Returns:
        int | float: Ergebnis
    """
    return float(node)
