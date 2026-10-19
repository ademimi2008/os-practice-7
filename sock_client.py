import socket
import sys

PATH = "/tmp/calc.sock"

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
try:
    s.connect(PATH)
except FileNotFoundError:
    sys.exit("Сервер не запущен")

with s, s.makefile("r") as f:
    def ask(expr):
        s.sendall((expr + "\n").encode())
        return f.readline().strip()

    if len(sys.argv) > 1:
        for e in sys.argv[1:]:
            print(f"{e} = {ask(e)}")
    else:
        try:
            while True:
                e = input("Выражение (пусто — выход): ").strip()
                if not e:
                    break
                print("Ответ:", ask(e))
        except (EOFError, KeyboardInterrupt):
            pass
