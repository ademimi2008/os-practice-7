import os
import signal
import socket
import sys
from common import safe_eval

PATH = "/tmp/calc.sock"

def handle(conn):
    me = os.getpid()
    print(f"[процесс {me}] клиент подключён")
    with conn, conn.makefile("r") as f:
        for line in f:
            expr = line.strip()
            res = safe_eval(expr)
            conn.sendall((res + "\n").encode())
            print(f"[процесс {me}] {expr} = {res}")
    print(f"[процесс {me}] клиент отключился")

if os.path.exists(PATH):
    os.unlink(PATH)

srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
srv.bind(PATH)
srv.listen()

def stop(*_):
    srv.close()
    if os.path.exists(PATH):
        os.unlink(PATH)
    print("\nСервер остановлен, сокет удалён")
    sys.exit(0)

signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)   # ядро само убирает зомби-процессы

print(f"Сервер слушает {PATH} (PID {os.getpid()})")
while True:
    conn, _ = srv.accept()
    pid = os.fork()
    if pid == 0:                                  # дочерний процесс
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        srv.close()                               # слушающий сокет ребёнку не нужен
        handle(conn)
        os._exit(0)
    else:                                         # родитель
        conn.close()                              # соединение обслуживает ребёнок
