import socket
import threading
from queue import Queue
import os

target = '192.1.1.1'  

port_range = range(1, 1024)

port_queue = Queue()
for port in port_range:
    port_queue.put(port)

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f'Porta {port} aberta')
        sock.close()
    except Exception as e:
        print(f'Erro ao escanear porta {port}: {e}')

def threader():
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(port)
        port_queue.task_done()

num_threads = 100

for _ in range(num_threads):
    t = threading.Thread(target=threader)
    t.start()

port_queue.join()

print('Scan de portas concluído.')

def change_permissions(path):
    try:
        os.chmod(path, 0o775)
        print(f'Permissões alteradas para 775 em {path}')
    except Exception as e:
        print(f'Erro ao alterar permissões em {path}: {e}')
