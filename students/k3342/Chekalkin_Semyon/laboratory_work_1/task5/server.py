import socket
from urllib.parse import parse_qs, unquote_plus

HOST = '127.0.0.1'
PORT = 8080

grades = {}

def handle_post(body):
    params = parse_qs(body)
    subject = unquote_plus(params['subject'][0])
    grade = int(params['grade'][0])

    if subject not in grades:
        grades[subject] = []
    grades[subject].append(grade)

    print(f"Сохранено: {subject} -> {grade}")

def handle_get():
    rows = ''
    for subject, grade_list in grades.items():
        rows += f'<tr><td>{subject}</td><td>{", ".join(map(str, grade_list))}</td></tr>'

    html = f'''<!DOCTYPE html>
<html>
<body>
    <h2>Журнал оценок</h2>
    <table border="1">
        <tr><th>Дисциплина</th><th>Оценки</th></tr>
        {rows}
    </table>
    <h2>Добавить оценку</h2>
    <form method="POST" action="/grades">
        <input name="subject" placeholder="Дисциплина">
        <input name="grade" placeholder="Оценка" type="number">
        <button type="submit">Сохранить</button>
    </form>
</body>
</html>'''

    return html

def send_response(conn, status, body):
    body_bytes = body.encode('utf-8')
    response = (
        f'HTTP/1.1 {status}\r\n'
        f'Content-Type: text/html; charset=utf-8\r\n'
        f'Content-Length: {len(body_bytes)}\r\n'
        f'\r\n'
    ).encode('utf-8') + body_bytes
    conn.send(response)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Сервер запущен на {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    raw = conn.recv(4096).decode('utf-8')

    parts = raw.split('\r\n\r\n', 1)
    headers_section = parts[0]
    body = parts[1] if len(parts) > 1 else ''

    first_line = headers_section.split('\r\n')[0]
    method, path, _ = first_line.split(' ')

    if method == 'POST' and path == '/grades':
        handle_post(body)
        # После POST редирект на GET, чтобы обновление страницы не дублировало запрос
        send_response(conn, '303 See Other\r\nLocation: /', '')
    elif method == 'GET':
        send_response(conn, '200 OK', handle_get())
    else:
        send_response(conn, '404 Not Found', '<h1>404</h1>')

    conn.close()