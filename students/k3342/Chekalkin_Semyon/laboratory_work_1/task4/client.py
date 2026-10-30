import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(conn):
    # Постоянное ожидание и вывод входящих сообщений
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Введите имя: ")
client.send(username.encode('utf-8'))

# Запуск потока для приёма сообщений
thread = threading.Thread(target=receive_messages, args=(client,))
thread.daemon = True
thread.start()

# Основной поток - отправка сообщений
while True:
    message = input()
    if message == '/quit':
        client.close()
        break
    client.send(f"{username}: {message}\n".encode('utf-8'))