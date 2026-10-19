import time
import numpy as np
from multiprocessing import Process, Pipe, Event, shared_memory

N = 10**7          # float64 → 80 МБ
REPEATS = 3

# ---------- разделяемая память ----------
def shm_reader(name, ready, res_conn):
    ready.wait()                                  # СИНХРОНИЗАЦИЯ: ждём, пока данные записаны
    shm = shared_memory.SharedMemory(name=name)
    arr = np.ndarray((N,), dtype=np.float64, buffer=shm.buf)
    local = arr.copy()                            # забираем данные себе
    t_end = time.perf_counter()
    del arr
    shm.close()
    res_conn.send((t_end, float(local.sum())))

def test_shm(data):
    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    ready = Event()
    a, b = Pipe()
    p = Process(target=shm_reader, args=(shm.name, ready, b))
    p.start()
    try:
        t0 = time.perf_counter()
        buf = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
        buf[:] = data
        ready.set()
        t_end, s = a.recv()
        p.join()
        del buf
    finally:
        shm.close()
        shm.unlink()                              # иначе сегмент останется в /dev/shm
    return t_end - t0, s

# ---------- Pipe ----------
def pipe_reader(conn, res_conn):
    raw = conn.recv_bytes()
    local = np.frombuffer(raw, dtype=np.float64)
    t_end = time.perf_counter()
    conn.close()
    res_conn.send((t_end, float(local.sum())))

def test_pipe(data):
    r, w = Pipe(duplex=False)
    a, b = Pipe()
    p = Process(target=pipe_reader, args=(r, b))
    p.start()
    r.close()          # закрываем ненужный конец в родителе (типичная ошибка!)
    t0 = time.perf_counter()
    w.send_bytes(memoryview(data))
    w.close()
    t_end, s = a.recv()
    p.join()
    return t_end - t0, s

if __name__ == "__main__":
    data = np.random.rand(N)
    ref = float(data.sum())
    print(f"Массив: {N} чисел float64, {data.nbytes / 2**20:.0f} МБ")

    for name, fn in [("shared_memory", test_shm), ("Pipe", test_pipe)]:
        times = []
        for _ in range(REPEATS):
            t, s = fn(data)
            assert abs(s - ref) < 1e-6 * abs(ref), "данные повреждены!"
            times.append(t)
        print(f"{name:14s}: лучшее {min(times):.3f} с, среднее {sum(times)/len(times):.3f} с")
