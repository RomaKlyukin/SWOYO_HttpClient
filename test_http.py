import json
from http_handle import HttpRequest, HttpResponse

def test_http_request() -> None:
    # Пример запроса на сервер

    # Создаем экземпляр HttpRequest
    request = HttpRequest(
        method='POST',
        target='/send_sms',
        headers={'Content-Type': 'application/json', 'Authorization': 'Basic YWRtaW46cm9vdA=='},
        body=json.dumps({'sender': '1234567890', 'recipient': '1234554321', 'message': 'Checking connection'})
    )
    
    # Ожидаемое байтовое представление запроса
    expected_bytes = (
        b'POST /send_sms HTTP/1.1\r\n'
        b'Content-Type: application/json\r\n'
        b'Authorization: Basic YWRtaW46cm9vdA==\r\n'
        b'\r\n'
        b'{"sender": "1234567890", "recipient": "1234554321", "message": "Checking connection"}'
    )
    
    # Проверяем, что метод to_bytes возвращает ожидаемые байты
    assert request.to_bytes() == expected_bytes

def test_http_response() -> None:
    # Пример байтового ответа от сервера
    response_bytes = (
        b'HTTP/1.1 200 OK\r\n'
        b'\r\n'
        b'{"status": "success", "message_id": "123456"}'
    )
    
    # Создаем экземпляр HttpResponse из байтового ответа
    response = HttpResponse.from_bytes(response_bytes)
    
    # Проверяем статус код и тело ответа
    assert response.status_code == 200
    assert response.body == {'status': 'success', 'message_id': '123456'}

def test_http_response_error() -> None:
    # Пример байтового ответа с ошибкой
    response_bytes = (
        b'HTTP/1.1 400 Bad Request\r\n'
        b'\r\n'
        b'{"error": "Invalid parameters"}'
    )
    
    # Создаем экземпляр HttpResponse из байтового ответа
    response = HttpResponse.from_bytes(response_bytes)
    
    # Проверяем статус код и тело ответа
    assert response.status_code == 400
    assert response.body == {'error': 'Invalid parameters'}