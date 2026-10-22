import os
import signal
import time

# 1. Создаем функцию-обработчик (добавили букву l в handler)
def handler(signum, frame):
    name = signal.Signals(signum).name
    print(f"\nПолучен {name}, но я не завершаюсь")

# 2. Регистрируем обработчик для сигнала SIGINT
signal.signal(signal.SIGINT, handler)

# 3. Выводим PID процесса
print("Мой PID:", os.getpid())

# 4. Бесконечный цикл, чтобы программа не закрывалась сама
while True:
    time.sleep(1)
