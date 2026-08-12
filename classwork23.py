# შექმენით Python პროგრამა, რომელიც რამდენიმე დამოუკიდებელ ასინქრონულ სამუშაოს მართავს.

# პროგრამაში უნდა არსებობდეს შემდეგი სამუშაოები:

# tasks = [
#     ("Downloading data", 3),
#     ("Processing data", 2),
#     ("Sending notification", 1),
#     ("Saving results", 4),
# ]

# თითოეული Task-ის მეორე მნიშვნელობა მიუთითებს, რამდენი წამი სჭირდება მის შესრულებას.

# ფუნქციამ უნდა:

# * დაბეჭდოს, რომ Task დაიწყო;
# * დაელოდოს მითითებულ დროს;
# * დაბეჭდოს, რომ Task დასრულდა;
# * დააბრუნოს შესრულების შედეგი.


# შეასრულეთ Task-ები თანმიმდევრულად

# შექმენით ფუნქცია, რომელიც ყველა Task-ს შეასრულებს ერთმანეთის მიყოლებით.

# გაზომეთ შესრულების საერთო დრო.

# შეასრულეთ Task-ები ასინქრონულად

# შექმენით მეორე ფუნქცია, რომელიც ყველა Task-ს ასინქრონულად შეასრულებს.

# კვლავ გაზომეთ შესრულების საერთო დრო.

# შემდეგ შეადარეთ ორივე შედეგი:

# Sequential execution time: X seconds
# Concurrent execution time: Y seconds

import asyncio
import time

tasks = [
    ("Downloading data", 3),
    ("Processing data", 2),
    ("Sending notification", 1),
    ("Saving results", 4),
]

async def perform_task(name, duration):
    print(f"{name} started")
    await asyncio.sleep(duration)
    print(f"{name} completed")
    return f"{name} result"

async def sequential_execution():
    start_time = time.perf_counter()
    results = []
    for name, duration in tasks:
        result = await perform_task(name, duration)
        results.append(result)
    total_time = time.perf_counter() - start_time
    print(f"Sequential execution time: {total_time:.2f} seconds")
    return results

async def concurrent_execution():
    start_time = time.perf_counter()
    task_coroutines = [perform_task(name, duration) for name, duration in tasks]
    results = await asyncio.gather(*task_coroutines)
    total_time = time.perf_counter() - start_time
    print(f"Concurrent execution time: {total_time:.2f} seconds")
    return results

sequential_results = asyncio.run(sequential_execution())
concurrent_results = asyncio.run(concurrent_execution())