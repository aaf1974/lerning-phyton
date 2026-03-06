"""
Python коллекции: comprehensions, Counter, dict.get()
======================================================
Аналогии C# → Python:
  list comprehension  = LINQ .Where().Select().ToList()
  dict comprehension  = dictionary initializer + LINQ
  set comprehension   = HashSet<T> через LINQ
  Counter             = Dictionary<T, int> + GroupBy().Count()
  dict.get(k, def)    = dict.GetValueOrDefault(key, default)
"""

from collections import Counter


# --- List comprehension = LINQ Where + Select ---

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# C#: numbers.Where(x => x % 2 == 0).Select(x => x * x).ToList()
even_squares = [x * x for x in numbers if x % 2 == 0]
assert even_squares == [4, 16, 36, 64, 100]

# C#: numbers.Select(x => x * 2).ToList()
doubled = [x * 2 for x in numbers]
assert doubled == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


# --- Dict comprehension = LINQ ToDictionary ---

words = ["apple", "banana", "cherry", "date"]

# C#: words.ToDictionary(w => w, w => w.Length)
word_lengths = {word: len(word) for word in words}
assert word_lengths["apple"] == 5
assert word_lengths["banana"] == 6

# Фильтрация: C#: words.Where(w => w.Length > 5).ToDictionary(...)
long_words = {word: len(word) for word in words if len(word) > 5}
assert "banana" in long_words
assert "date" not in long_words


# --- Set comprehension = HashSet<T> ---

# C#: new HashSet<int>(numbers.Select(x => x % 3))
remainders = {x % 3 for x in numbers}
assert remainders == {0, 1, 2}


# --- Counter = Dictionary<T,int> + GroupBy ---

text = "mississippi"
# C#: text.GroupBy(c => c).ToDictionary(g => g.Key, g => g.Count())
letter_count = Counter(text)
assert letter_count["s"] == 4
assert letter_count["p"] == 2
assert letter_count.most_common(1) == [("s", 4)]

orders_statuses = ["pending", "shipped", "pending", "delivered", "shipped", "pending"]
status_count = Counter(orders_statuses)
assert status_count["pending"] == 3


# --- dict.get() = GetValueOrDefault ---

config = {"host": "localhost", "port": 5432}

# C#: config.GetValueOrDefault("host", "unknown")
host = config.get("host", "unknown")
assert host == "localhost"

# C#: config.GetValueOrDefault("timeout", 30)
timeout = config.get("timeout", 30)
assert timeout == 30

# Вложенный get с fallback
nested = {"db": {"host": "localhost"}}
db_config = nested.get("db", {})
db_host = db_config.get("host", "127.0.0.1")
assert db_host == "localhost"


if __name__ == "__main__":
    print("=== task_1_collections.py ===")
    print(f"even_squares: {even_squares}")
    print(f"word_lengths: {word_lengths}")
    print(f"letter_count top-3: {letter_count.most_common(3)}")
    print(f"status_count: {dict(status_count)}")
    print("Все assert прошли!")
