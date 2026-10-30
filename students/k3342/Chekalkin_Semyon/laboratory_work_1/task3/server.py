import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 9090

INDEX_PATH = Path(__file__).parent / "index.html"


def build_response():
    html_bytes = INDEX_PATH.read_bytes()

    status = "HTTP/1.1 200 OK"
    type_header = "Content-Type: text/html; charset=utf-8"
    len_header = f"Content-Length: {len(html_bytes)}"
    connection_header = "Connection: close"

    headers = (
        status + "\r\n"
        + type_header + "\r\n"
        + len_header + "\r\n"
        + connection_header + "\r\n"
        + "\r\n"
    )
    return headers.encode("utf-8") + html_bytes


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    print(f"Сервер запущен на {HOST}:{PORT}. Остановка: Ctrl+C")

    sock.listen(5)
    print("Ожидаю подключения браузера...")

    try:
        while True:
            conn, addr = sock.accept()
            with conn:
                request = conn.recv(1024)
                if not request:
                    # браузер открыл соединение, но ничего не отправил
                    continue

                print("Подключился клиент:", addr)
                print(request.split(b"\r\n", 1)[0].decode("utf-8", errors="replace"))

                conn.sendall(build_response())
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
