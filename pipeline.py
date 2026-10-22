
import subprocess

# 1. Запускаем команду 'ls' (вывод списка файлов)
p1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)

# 2. Запускаем команду 'grep py', передавая ей на вход (stdin) вывод от p1
p2 = subprocess.Popen(["grep", "py"], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)

# 3. Закрываем дескриптор в родителе, чтобы p1 не завис
p1.stdout.close()

# 4. Читаем итоговый результат из p2
out, _ = p2.communicate()

# 5. Ожидаем корректного завершения первого процесса
p1.wait()

# 6. Выводим результат на экран
print(out)
