"""
Python match/case — структурное сопоставление с образцом
=========================================================
Аналогии C# → Python:
  switch expression (C# 8+)  = match/case
  pattern matching (C# 9+)   = match/case с деструктуризацией
  guard condition (C# when)  = match/case if (guard)
  _ (discard)                = case _: (default)
"""

from dataclasses import dataclass
from enum import Enum


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class HttpRequest:
    method: str
    path: str
    status_code: int = 200


def describe_http_status(code: int) -> str:
    """
    Описывает HTTP статус код.

    C# аналог (switch expression):
        string desc = code switch {
            200 => "OK",
            201 => "Created",
            >= 400 and < 500 => "Client Error",
            >= 500 => "Server Error",
            _ => "Unknown"
        };
    """
    match code:
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 204:
            return "No Content"
        case 301 | 302:
            return "Redirect"
        case 400:
            return "Bad Request"
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not Found"
        case 422:
            return "Unprocessable Entity"
        case code if 400 <= code < 500:  # guard condition = C# 'when'
            return f"Client Error ({code})"
        case code if 500 <= code < 600:
            return f"Server Error ({code})"
        case _:
            return "Unknown"


def route_request(request: HttpRequest) -> str:
    """
    Маршрутизация запросов.

    C# аналог (switch expression с pattern matching):
        string result = request switch {
            { Method: "GET", Path: "/health" } => "health check",
            { Method: "POST" } => "create resource",
            ...
        };
    """
    match request:
        case HttpRequest(method="GET", path="/health"):
            return "health check"
        case HttpRequest(method="GET", path=path) if path.startswith("/orders"):
            return f"list/get orders: {path}"
        case HttpRequest(method="POST", path="/orders"):
            return "create order"
        case HttpRequest(method="PUT", path=path) if "/orders/" in path:
            return f"update order: {path}"
        case HttpRequest(method="DELETE"):
            return "delete resource"
        case _:
            return "unknown route"


def classify_value(value: object) -> str:
    """
    Классификация значений по типу (C# type patterns).

    C# аналог:
        string desc = value switch {
            int n when n < 0 => "negative int",
            int n => $"positive int: {n}",
            string s => $"string: {s}",
            null => "null",
            _ => "other"
        };
    """
    match value:
        case None:
            return "null"
        case int(n) if n < 0:
            return f"negative int: {n}"
        case int(n):
            return f"positive int: {n}"
        case float(f):
            return f"float: {f:.2f}"
        case str(s) if len(s) == 0:
            return "empty string"
        case str(s):
            return f"string: {s!r}"
        case [*items]:
            return f"list with {len(items)} items"
        case {"type": t, **rest}:
            return f"dict with type={t!r}, keys={list(rest.keys())}"
        case _:
            return f"other: {type(value).__name__}"


# --- Assert-тесты ---

# HTTP статусы
assert describe_http_status(200) == "OK"
assert describe_http_status(201) == "Created"
assert describe_http_status(204) == "No Content"
assert describe_http_status(301) == "Redirect"
assert describe_http_status(302) == "Redirect"
assert describe_http_status(400) == "Bad Request"
assert describe_http_status(404) == "Not Found"
assert describe_http_status(429) == "Client Error (429)"
assert describe_http_status(503) == "Server Error (503)"
assert describe_http_status(999) == "Unknown"

# Маршрутизация
assert route_request(HttpRequest("GET", "/health")) == "health check"
assert route_request(HttpRequest("GET", "/orders/123")) == "list/get orders: /orders/123"
assert route_request(HttpRequest("POST", "/orders")) == "create order"
assert route_request(HttpRequest("PUT", "/orders/456")) == "update order: /orders/456"
assert route_request(HttpRequest("DELETE", "/orders/1")) == "delete resource"

# Классификация
assert classify_value(None) == "null"
assert classify_value(-5) == "negative int: -5"
assert classify_value(42) == "positive int: 42"
assert classify_value("hello") == "string: 'hello'"
assert classify_value("") == "empty string"
assert classify_value([1, 2, 3]) == "list with 3 items"
assert classify_value({"type": "order", "id": 1}) == "dict with type='order', keys=['id']"


if __name__ == "__main__":
    print("=== task_3_pattern_matching.py ===")
    for code in [200, 201, 301, 400, 404, 429, 500, 503, 999]:
        print(f"  {code}: {describe_http_status(code)}")
    print()
    requests = [
        HttpRequest("GET", "/health"),
        HttpRequest("GET", "/orders/123"),
        HttpRequest("POST", "/orders"),
        HttpRequest("PUT", "/orders/456"),
        HttpRequest("DELETE", "/orders/1"),
    ]
    for req in requests:
        print(f"  {req.method} {req.path} → {route_request(req)}")
    print("Все assert прошли!")
