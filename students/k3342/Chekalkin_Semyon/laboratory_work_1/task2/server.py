import socket
import json
import math
import cmath

HOST = "127.0.0.1"
PORT = 9090


def solve_quadratic(a, b, c):
    # Решение ax^2 + bx + c = 0; Возврат (дискриминант, [(re, im), ...])
    d = b * b - 4 * a * c
    if d >= 0:
        sqrt_d = math.sqrt(d)
    else:
        sqrt_d = cmath.sqrt(d)

    # "+ 0.0" превращает -0.0 в 0.0
    roots = []
    for root in ((-b + sqrt_d) / (2 * a), (-b - sqrt_d) / (2 * a)):
        roots.append([root.real + 0.0, root.imag + 0.0] if isinstance(root, complex)
                     else [root + 0.0, 0.0])
    return d, roots


def process(data):
    # Разбирает запрос и возвращает словарь-ответ
    try:
        params = json.loads(data.decode("utf-8"))

        if not isinstance(params, list) or len(params) != 3:
            raise ValueError("Нужно передать три коэффициента.")

        if not all(
            isinstance(x, (int, float)) and
            not isinstance(x, bool) and math.isfinite(x)
            for x in params
        ):
            raise ValueError("Коэффициенты должны быть конечными числами.")

        if params[0] == 0:
            raise ValueError("Коэффициент a не должен быть равен нулю.")

        d, roots = solve_quadratic(*params)
        if not math.isfinite(d):
            raise ValueError("Слишком большие коэффициенты.")

        print("Дискриминант:", d, "Корни:", roots)
        return {"ok": True, "discriminant": d, "roots": roots}

    except (ValueError, TypeError, OverflowError, ZeroDivisionError) as e:
        return {"ok": False, "error": str(e)}


def handle_client(conn, addr):
    with conn:
        print("Подключился клиент:", addr)

        chunks = []
        while True:
            part = conn.recv(1024)
            if not part:
                break
            chunks.append(part)

        response = process(b"".join(chunks))
        conn.sendall(json.dumps(response).encode("utf-8"))

    print("Соединение закрыто.")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"Сервер ожидает подключения на {HOST}:{PORT}. Остановка: Ctrl+C")

    try:
        while True:
            conn, addr = sock.accept()
            try:
                handle_client(conn, addr)
            except OSError as e:
                print("Ошибка соединения:", e)
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
