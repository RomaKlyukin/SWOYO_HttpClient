# CLI-client for sending SMS messages

Клонируем репозиторий и переходим в директорию SWOYO_HttpClient:
```cmd
git clone https://github.com/RomaKlyukin/SWOYO_HttpClient
cd SWOYO_HttpClient
```

Создаем и активируем виртуальное окружение:
```cmd
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Подключаемся к мок-серверу:
```cmd
./prism-cli-win.exe mock sms-platform.yaml

[20:12:01] » [CLI] ...  awaiting  Starting Prism…
[20:12:01] » [CLI] i  info      POST       http://127.0.0.1:4010/send_sms
[20:12:01] » [CLI] ►  start     Prism is listening on http://127.0.0.1:4010
```

Запускаем приложение в консоли, указав параметры:
```cmd
python main.py 12345 54321 "Пример"

Код ответа: 200
Тело ответа: {'status': 'success', 'message_id': '123456'}
```
