import json
import socket
import re
import base64
from http_handle import HttpRequest, HttpResponse


class SMSService:
    def __init__(self, url: str, username: str, password: str) -> None:
        self.url = url
        self.username = username
        self.password = password

    def send_sms(self, sender: str, recipient: str, message: str) -> HttpResponse:
        """
        Отправляет сообщение в виде http-запроса на сервер и получает http-ответ
        """

        # Кодируем имя пользователя и пароль
        username_password = f"{self.username}:{self.password}"
        username_password = base64.b64encode(username_password.encode()).decode()

        # Выделяем хост, порт и путь сервера
        pattern = re.findall(r"http://(.*)(/.*)", self.url)
        host, port = pattern[0][0].split(':')
        path = pattern[0][1]

        # Формируем тело запроса
        body = json.dumps({"sender": sender, "recipient": recipient, "message": message})

        # Формируем заголовок запроса
        headers = {
            "Host": f"{host}:{port}",
            "Content-Type": "application/json",
            "Content-Length": str(len(body)),
            "Authorization": f"Basic {username_password}"
        }

        # Формируем запрос
        request = HttpRequest("POST", path, headers, body)

        # Производим отправку сообщения с помощью сокетов
        client_sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # Создаем клиентский сокет

        # Подключаемся к серверу
        if client_sock.connect_ex((host, int(port))) > 0:
            # Возвращаем -1 при проваленной попытке соединения
            return -1

        client_sock.sendall(request.to_bytes()) # Отправляем запрос
        data = client_sock.recv(1024)           # Получаем ответ от сервера
        client_sock.close()                     # Прерываем соединение

        return HttpResponse.from_bytes(data)
