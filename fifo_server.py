import os
import signal
import sys
from common import safe_eval

REQ = "/tmp/calc_req.fifo"

def cleanup(*_):
    if os.path.exists(REQ):
        os.unlink(REQ)
    print("\nСервер остановлен, FIFO удалён")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

if not os.path.exists(REQ):
    os.mkfifo(REQ, 0o666)
print(f"Сервер ждёт запросы в {REQ} (Ctrl+C — выход)")

while True:
    # open() блокируется, пока FIFO не откроет хотя бы один писатель — это нормально
    with open(REQ, "r") as req:
        for line in req:            # EOF — когда все писатели закрыли канал
            line = line.strip()
            if not line or "|" not in line:
                continue
            pid, expr = line.split("|", 1)
            result = safe_eval(expr)
            resp = f"/tmp/calc_resp_{pid}.fifo"
            if os.path.exists(resp):
                with open(resp, "w") as r:
                    r.write(result + "\n")
            print(f"[клиент {pid}] {expr} = {result}")
    # клиенты отключились — снова открываем FIFO и ждём следующего
