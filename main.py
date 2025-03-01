import tomllib
import sys

from sms_service import SMSService


# Выгружаем параметры конфигурации
def load_config(file_path) -> dict:
    """
    Выгружает параметры конфигурации из файла .toml
    """
    with open(file_path, "rb") as f:
        return tomllib.load(f)


def main() -> None:
    
    # Сохраняем записанные параметры  из командной строки
    params = sys.argv

    # Передаем параметры конфигурации
    config = load_config("config.toml")
    sms_service = SMSService(config["url"], config["username"], config["password"])

    # Отправляем сообщение и получаем Http-ответ
    response = sms_service.send_sms(params[1], params[2], params[3])

    # Проверяем смогли ли мы подключиться к серверу и получить ответ
    if response == -1:
        print("Не удалось подключиться к серверу")
    else:
        print(f"Код ответа: {response.status_code}\nТело ответа: {response.body}")


if __name__ == "__main__":
    main()
