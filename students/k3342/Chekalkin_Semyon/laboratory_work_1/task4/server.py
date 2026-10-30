import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# Словарь активных клиентов: { socket: username }
clients = {}
lock = threading.Lock()

def broadcast(message, sender_conn):
    # Рассылка сообщения всем клиентам, кроме отправителя
    with lock:
        for conn in clients:
            if conn != sender_conn:
                conn.send(message)

def handle_client(conn):
    while True:
        try:
            message = conn.recv(1024)
            if not message:
                break
            broadcast(message, conn)
        except:
            break

    # Клиент отключился — удаление из словаря и уведомление остальных
    with lock:
        username = clients.pop(conn)
    conn.close()
    broadcast(f"{username} покинул чат.\n".encode('utf-8'), conn)
    print(f"[-] {username} отключился")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Сервер запущен на {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    # Получение имени пользователя при подключении
    username = conn.recv(1024).decode('utf-8')

    with lock:
        clients[conn] = username

    print(f"[+] {username} подключился ({addr})")

    # Запуск потока для обработки клиента
    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.daemon = True
    thread.start()