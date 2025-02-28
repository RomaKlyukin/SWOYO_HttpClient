import json

class HttpRequest:
    def __init__(
        self, method: str, target: str, headers: dict, body: dict, version: str = "HTTP/1.1"
    ) -> None:
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        starting_line = f"{self.method} {self.target} {self.version}\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())
        body = json.dumps(self.body)
        return (starting_line + headers + "\r\n" + body).encode()


class HttpResponse:
    def __init__(self, status_code: int, body: dict) -> None:
        self.status_code = status_code
        self.body = body

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        data = binary_data.decode().split("\r\n\r\n", 1)
        starting_line = data[0].split("\r\n", 1)[0]
        status_code = int(starting_line.split()[1])
        if len(data) > 1:
            body = json.loads(data[1])
        else:
            body = {}
        return cls(status_code, body)
