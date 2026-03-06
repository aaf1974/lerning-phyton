"""
asyncio.gather() = Task.WhenAll()
==================================
Аналогии C# → Python:
  async Task<T> Method()     = async def method() -> T:
  await Method()              = await method()
  Task.WhenAll(t1, t2, t3)   = asyncio.gather(t1(), t2(), t3())
  Task.WhenAny(...)           = asyncio.wait(..., return_when=FIRST_COMPLETED)
  new SemaphoreSlim(3)        = asyncio.Semaphore(3)
  await semaphore.WaitAsync() = async with semaphore:

КРИТИЧНО: coroutine без await — это ОБЪЕКТ, не результат!
  C#:  var task = FetchUser(1);  // задача ЗАПУЩЕНА
  Py:  coro = fetch_user(1)      # корутина НЕ запущена — это просто объект!
       result = await coro       # вот теперь выполняется
"""

import asyncio
import time
from typing import TypedDict


class UserData(TypedDict):
    id: int
    name: str
    email: str


async def fetch_user(user_id: int) -> UserData:
    """
    Имитация асинхронного запроса к API/БД.

    C# аналог:
        async Task<UserData> FetchUserAsync(int userId) {
            await Task.Delay(100);
            return new UserData { Id = userId, ... };
        }

    ВНИМАНИЕ: fetch_user(1) возвращает coroutine object, НЕ данные!
    Данные появляются только после await fetch_user(1).
    """
    await asyncio.sleep(0.1)  # имитация задержки сети/БД
    return UserData(
        id=user_id,
        name=f"User {user_id}",
        email=f"user{user_id}@example.com",
    )


async def fetch_sequential(user_ids: list[int]) -> list[UserData]:
    """
    Последовательная загрузка — каждый запрос ждёт предыдущего.

    C# аналог (плохой вариант):
        var results = new List<UserData>();
        foreach (var id in ids)
            results.Add(await FetchUserAsync(id));  // ждём каждый!

    Время: N * 0.1 секунды
    """
    results = []
    for uid in user_ids:
        user = await fetch_user(uid)  # ждём каждый запрос
        results.append(user)
    return results


async def fetch_parallel(user_ids: list[int]) -> list[UserData]:
    """
    Параллельная загрузка через gather — все запросы одновременно.

    C# аналог (правильный вариант):
        var tasks = ids.Select(id => FetchUserAsync(id));
        var results = await Task.WhenAll(tasks);

    Время: ~0.1 секунды независимо от количества запросов
    """
    # gather запускает все корутины одновременно и ждёт всех
    results = await asyncio.gather(*[fetch_user(uid) for uid in user_ids])
    return list(results)


async def fetch_with_semaphore(
    user_ids: list[int],
    max_concurrent: int = 3,
) -> list[UserData]:
    """
    Ограничение параллелизма через Semaphore.

    C# аналог:
        var semaphore = new SemaphoreSlim(3);
        async Task<UserData> FetchWithLimit(int id) {
            await semaphore.WaitAsync();
            try { return await FetchUserAsync(id); }
            finally { semaphore.Release(); }
        }
        var results = await Task.WhenAll(ids.Select(FetchWithLimit));

    Полезно когда:
    - Есть rate limiting у внешнего API
    - Нужно ограничить нагрузку на БД
    - Слишком много одновременных соединений
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_limited(uid: int) -> UserData:
        async with semaphore:  # автоматически acquire/release
            return await fetch_user(uid)

    results = await asyncio.gather(*[fetch_limited(uid) for uid in user_ids])
    return list(results)


async def demonstrate_coroutine_object() -> None:
    """
    Демонстрация КЛЮЧЕВОГО отличия от C#:
    корутина без await — это объект, а не результат!
    """
    print("\n=== Корутина без await — объект, не результат! ===")

    # C#: var task = FetchUserAsync(1);  // задача СРАЗУ запущена в фоне
    # Python:
    coro = fetch_user(1)  # fetch_user НЕ вызвана! Это просто объект
    print(f"  type(coro) = {type(coro)}")  # <class 'coroutine'>
    print(f"  coro = {coro}")              # <coroutine object fetch_user ...>

    # Теперь выполняем:
    result = await coro  # вот здесь fetch_user реально работает
    print(f"  await coro → {result['name']}")

    # Нельзя await дважды!
    # await coro  # → RuntimeError: cannot reuse already awaited coroutine


async def main() -> None:
    user_ids = list(range(1, 6))  # [1, 2, 3, 4, 5]

    # --- Демонстрация корутины как объекта ---
    await demonstrate_coroutine_object()

    # --- Последовательно ---
    print(f"\n=== Последовательно ({len(user_ids)} запросов) ===")
    start = time.perf_counter()
    seq_results = await fetch_sequential(user_ids)
    seq_time = time.perf_counter() - start
    print(f"  Результатов: {len(seq_results)}, Время: {seq_time:.2f}s")
    assert len(seq_results) == len(user_ids)

    # --- Параллельно через gather ---
    print(f"\n=== Параллельно — asyncio.gather() ===")
    start = time.perf_counter()
    par_results = await fetch_parallel(user_ids)
    par_time = time.perf_counter() - start
    print(f"  Результатов: {len(par_results)}, Время: {par_time:.2f}s")
    print(f"  Ускорение: {seq_time / par_time:.1f}x")
    assert len(par_results) == len(user_ids)
    assert par_time < seq_time  # параллельно быстрее

    # --- С Semaphore (макс 2 одновременно) ---
    print(f"\n=== С Semaphore(max_concurrent=2) ===")
    start = time.perf_counter()
    sem_results = await fetch_with_semaphore(user_ids, max_concurrent=2)
    sem_time = time.perf_counter() - start
    print(f"  Результатов: {len(sem_results)}, Время: {sem_time:.2f}s")
    assert len(sem_results) == len(user_ids)

    print("\n=== Итог ===")
    print(f"  Sequential:  {seq_time:.2f}s")
    print(f"  Parallel:    {par_time:.2f}s  ← asyncio.gather() = Task.WhenAll()")
    print(f"  Semaphore-2: {sem_time:.2f}s  ← SemaphoreSlim(2)")


if __name__ == "__main__":
    asyncio.run(main())
