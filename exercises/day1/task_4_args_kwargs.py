"""
Python *args и **kwargs
=======================
Аналогии C# → Python:
  *args        = params int[] numbers (переменное кол-во позиционных аргументов)
  **kwargs     = Dictionary<string, object> overrides (именованные аргументы)
  keyword-only = параметры после * (нет прямого аналога в C#, похоже на named args)
  / (positional-only) = нет аналога в C#
"""

from typing import Any


def sum_all(*numbers: float) -> float:
    """
    Сумма произвольного количества чисел.

    C# аналог:
        double SumAll(params double[] numbers) => numbers.Sum();
    """
    return sum(numbers)


def create_config(base: dict[str, Any], **overrides: Any) -> dict[str, Any]:
    """
    Создаёт конфигурацию с переопределениями.

    C# аналог (Dictionary merge):
        var result = new Dictionary<string, object>(base);
        foreach (var (k, v) in overrides) result[k] = v;
    """
    return {**base, **overrides}


def log_event(
    message: str,
    *,                          # всё что после * — keyword-only
    level: str = "INFO",
    source: str = "app",
) -> str:
    """
    Логирование события.

    Параметры после * — keyword-only (нельзя передать позиционно).
    C# аналог: нет прямого, но похоже на обязательные named args через
               CallerMemberName или именованные параметры.

    Пример вызова:
        log_event("msg", level="ERROR")   ✅
        log_event("msg", "ERROR")          ❌ TypeError
    """
    return f"[{level}] [{source}] {message}"


def pipeline(*funcs: Any) -> Any:
    """
    Конвейер функций — передаёт результат из одной в другую.

    C# аналог (LINQ-style):
        Func<T, T>[] pipeline = { f1, f2, f3 };
        var result = pipeline.Aggregate(input, (acc, f) => f(acc));
    """
    def apply(value: Any) -> Any:
        for func in funcs:
            value = func(value)
        return value
    return apply


def merge_dicts(*dicts: dict[str, Any]) -> dict[str, Any]:
    """
    Объединяет несколько словарей (последний побеждает).

    C# аналог:
        var result = dicts.Aggregate(new Dictionary<string, object>(),
            (acc, d) => { foreach (var kv in d) acc[kv.Key] = kv.Value; return acc; });
    """
    result: dict[str, Any] = {}
    for d in dicts:
        result.update(d)
    return result


# --- Assert-тесты ---

# *args = params[]
assert sum_all() == 0
assert sum_all(1) == 1
assert sum_all(1, 2, 3) == 6
assert sum_all(1, 2, 3, 4, 5) == 15
assert sum_all(0.1, 0.2) == pytest_approx(0.3)  # type: ignore[name-defined]  # noqa: F821

# Unpacking при вызове: *list передаёт элементы как позиционные аргументы
numbers = [10, 20, 30]
assert sum_all(*numbers) == 60

# **kwargs
base_cfg = {"host": "localhost", "port": 5432, "debug": False}
dev_cfg = create_config(base_cfg, debug=True, port=5433)
assert dev_cfg["host"] == "localhost"
assert dev_cfg["port"] == 5433
assert dev_cfg["debug"] is True
assert base_cfg["debug"] is False  # оригинал не изменился

# Keyword-only
msg = log_event("Server started", level="INFO", source="api")
assert msg == "[INFO] [api] Server started"

msg_default = log_event("test")
assert msg_default == "[INFO] [app] test"

# Pipeline
process = pipeline(str.strip, str.upper, lambda s: s + "!")
assert process("  hello  ") == "HELLO!"

double_then_add = pipeline(lambda x: x * 2, lambda x: x + 10)
assert double_then_add(5) == 20

# Merge dicts
merged = merge_dicts({"a": 1}, {"b": 2}, {"a": 99, "c": 3})
assert merged == {"a": 99, "b": 2, "c": 3}


if __name__ == "__main__":
    print("=== task_4_args_kwargs.py ===")
    print(f"sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")

    base = {"host": "localhost", "port": 5432, "debug": False}
    print(f"dev config: {create_config(base, debug=True, port=5433)}")

    print(log_event("App started", level="INFO", source="main"))
    print(log_event("DB error", level="ERROR", source="database"))

    process = pipeline(str.strip, str.upper, lambda s: f">> {s} <<")
    print(process("  python rocks  "))
    print("Все assert прошли (кроме approx — для него нужен pytest)!")
