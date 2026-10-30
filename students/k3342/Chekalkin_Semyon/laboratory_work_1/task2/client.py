import socket
import json
import math

try:
    nums = [float(x) for x in input(
        "Введите коэффициенты a, b, c через пробел: "
    ).split()]

    if len(nums) != 3:
        raise ValueError("Нужно ввести ровно три коэффициента.")

    if not all(map(lambda x:math.isfinite(x), nums)):
        raise ValueError("Коэффициенты должны быть конечными числами.")

    if nums[0] == 0:
        raise ValueError("Коэффициент a не должен быть равен нулю.")

except ValueError as e:
    print("Ошибка ввода:", e)
    raise SystemExit

data = json.dumps(nums).encode("utf-8")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("127.0.0.1", 9090))
    sock.sendall(data)

    sock.shutdown(socket.SHUT_WR)

    chunks = []
    while True:
        part = sock.recv(1024)
        if not part:
            break
        chunks.append(part)

data_recv = b"".join(chunks)
response = json.loads(data_recv.decode("utf-8"))

def format_root(re, im):
    if im == 0:
        return f"{re:.10g}"
    sign = "+" if im >= 0 else "-"
    return f"{re:.10g} {sign} {abs(im):.10g}i"


if response["ok"]:
    print("Дискриминант:", f"{response['discriminant']:.10g}")
    print("Корни уравнения:", ", ".join(format_root(re, im) for re, im in response["roots"]))
else:
    print("Ошибка:", response["error"])
