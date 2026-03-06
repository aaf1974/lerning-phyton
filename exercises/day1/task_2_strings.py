"""
Python f-strings и форматирование строк
=======================================
Аналогии C# → Python:
  $"Hello {name}"        = f"Hello {name}"
  $"{amount:N2}"         = f"{amount:,.2f}"
  String.Format("{0,-10}", s) = f"{s:<10}"
  {val=}                 = debug output (Python 3.8+, нет аналога в C#)
"""


def format_money(amount: float, currency: str = "USD") -> str:
    """
    Форматирует денежную сумму.

    C# аналог:
        $"{amount:N2} {currency}"
        или: amount.ToString("N2") + " " + currency
    """
    return f"{amount:,.2f} {currency}"


def format_table_row(name: str, amount: float, status: str) -> str:
    """
    Форматирует строку таблицы с выравниванием.

    C# аналог:
        String.Format("{0,-20} {1,12} {2,-10}", name, amount, status)
        или: $"{name,-20} {amount,12:N2} {status,-10}"
    """
    return f"{name:<20} {amount:>12,.2f} {status:<10}"


def debug_values(**kwargs: object) -> str:
    """
    Debug-вывод значений переменных.

    C# аналог: нет прямого — ближайший nameof() + интерполяция
    Python 3.8+: f"{variable=}" автоматически пишет "variable=значение"
    """
    parts = []
    for key, value in kwargs.items():
        parts.append(f"{key}={value!r}")
    return ", ".join(parts)


# --- Базовые f-strings ---

name = "Alice"
age = 30
greeting = f"Привет, {name}! Тебе {age} лет."
assert greeting == "Привет, Alice! Тебе 30 лет."

# Выражения прямо в f-string (C#: нет, нужен метод)
result = f"2 + 2 = {2 + 2}"
assert result == "2 + 2 = 4"

# Методы в f-string
assert f"{name.upper()}" == "ALICE"
assert f"{name!r}" == "'Alice'"  # repr() — аналог ToString() с кавычками


# --- Числовое форматирование ---

price = 1234567.89

# C#: $"{price:N2}" → "1,234,567.89"
assert f"{price:,.2f}" == "1,234,567.89"

# C#: $"{price:C}" (зависит от локали)
assert format_money(price) == "1,234,567.89 USD"
assert format_money(99.9, "EUR") == "99.90 EUR"
assert format_money(0.5, "RUB") == "0.50 RUB"

# Процент: C#: $"{0.1234:P1}" → "12.3 %"
ratio = 0.1234
assert f"{ratio:.1%}" == "12.3%"

# Целые числа
count = 1000000
assert f"{count:,}" == "1,000,000"  # C#: $"{count:N0}"


# --- Выравнивание (аналог String.PadLeft/PadRight) ---

# C#: name.PadRight(20)
assert f"{'Alice':<20}" == "Alice               "

# C#: "42".PadLeft(6, '0')
assert f"{42:06d}" == "000042"

# C#: value.ToString().PadLeft(10)
assert f"{price:>15,.2f}" == "  1,234,567.89"


# --- Таблица заказов ---

header = f"{'Заказчик':<20} {'Сумма':>12} {'Статус':<10}"
row1 = format_table_row("Иван Иванов", 15000.50, "shipped")
row2 = format_table_row("Мария Петрова", 3200.00, "pending")

assert "Иван Иванов" in row1
assert "15,000.50" in row1


# --- Debug format {val=} ---

x = 42
pi = 3.14159
# f"{x=}" выводит "x=42" — имя переменной + значение
debug_str = f"{x=}, {pi=:.2f}"
assert debug_str == "x=42, pi=3.14"


if __name__ == "__main__":
    print("=== task_2_strings.py ===")
    print(f"{format_money(1234567.89)}")
    print(f"{format_money(99.9, 'EUR')}")
    print()
    print(f"{'Заказчик':<20} {'Сумма':>12} {'Статус':<10}")
    print("-" * 44)
    print(format_table_row("Иван Иванов", 15000.50, "shipped"))
    print(format_table_row("Мария Петрова", 3200.00, "pending"))
    print()
    x, y = 10, 20
    print(f"Debug: {x=}, {y=}, {x+y=}")
    print("Все assert прошли!")
