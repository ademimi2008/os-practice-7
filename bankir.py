
AVAILABLE = [3, 3, 2]

ALLOCATION = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

MAX = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

def is_safe(available, allocation, maximum):
    n, m = len(allocation), len(available)

    need = [
        [maximum[i][j] - allocation[i][j] for j in range(m)]
        for i in range(n)
    ]

    work = available[:]
    finish = [False] * n
    order = []
    progress = True

    while progress:
        progress = False
        for i in range(n):
            if not finish[i] and all(
                need[i][j] <= work[j] for j in range(m)
            ):
                for j in range(m):
                    work[j] += allocation[i][j]
                finish[i] = True
                order.append(f"P{i}")
                progress = True

    return all(finish), order

safe, order = is_safe(AVAILABLE, ALLOCATION, MAX)

if safe:
    print("Система находится в безопасном состоянии.")
    print("Безопасная последовательность:", " -> ".join(order))
else:
    print("Система находится в небезопасном состоянии.")