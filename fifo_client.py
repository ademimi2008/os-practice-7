import os
import sys

REQ = "/tmp/calc_req.fifo"
pid = os.getpid()
RESP = f"/tmp/calc_resp_{pid}.fifo"

if not os.path.exists(REQ):
    sys.exit("Сначала запусти fifo_server.py")

os.mkfifo(RESP, 0o600)

try:
    while True:
        expr = input("Выражение (пусто — выход): ").strip()
        if not expr:
            break

        with open(REQ, "w") as req:
            req.write(f"{pid}|{expr}\n")

        with open(RESP, "r") as r:
            print("Ответ:", r.readline().strip())

finally:
    if os.path.exists(RESP):
        os.unlink(RESP)
    print("Клиент завершён")
