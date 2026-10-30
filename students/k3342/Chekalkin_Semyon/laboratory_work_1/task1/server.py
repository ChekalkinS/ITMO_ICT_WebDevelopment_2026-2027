import socket

HOST = "127.0.0.1"
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.bind((HOST, PORT))
    print(f"UDP-сервер запущен на {HOST}:{PORT}. Остановка: Ctrl+C")

    try:
        while True:
            data, address = sock.recvfrom(1024)
            message = data.decode("utf-8", errors="replace")
            print(f"Сервер получил от {address}: {message}")

            answer = "Hello, client"
            sock.sendto(answer.encode("utf-8"), address)
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
