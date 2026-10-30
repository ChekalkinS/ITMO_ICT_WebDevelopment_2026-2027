import socket

SERVER_ADDRESS = ("127.0.0.1", 9090)
TIMEOUT = 5

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    # ожидание ответа ограниченное время, тк UDP не гарантирует доставку
    sock.settimeout(TIMEOUT)

    message = "Hello, server"
    sock.sendto(message.encode("utf-8"), SERVER_ADDRESS)
    print("Клиент отправил:", message)

    try:
        data_recv, address = sock.recvfrom(1024)
    except socket.timeout:
        print(f"Ответ не получен за {TIMEOUT} с: сервер недоступен или пакет потерян.")
    except ConnectionResetError:
        print("Сервер недоступен (порт закрыт). Запустите server.py.")
    else:
        print("Клиент получил:", data_recv.decode("utf-8", errors="replace"))
