import tomllib
import sys
import logging

from sms_service import SMSService

# Настраиваем сисетму логирования
logging.basicConfig(level=logging.INFO, filename="sms_client.log", filemode="a",
                    format="[%(asctime)s: %(levelname)s] %(message)s", encoding='utf-8')

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

    if len(params) - 1 != 3:
        print("Передано неверное количество параметров")
        return

    # Передаем параметры конфигурации
    config = load_config("config.toml")
    sms_service = SMSService(config["url"], config["username"], config["password"])

    logging.info(f"Номер отправителя: {params[1]} | Номер получателя: {params[2]} | Сообщение: {params[3]}")

    # Отправляем сообщение и получаем Http-ответ
    response = sms_service.send_sms(params[1], params[2], params[3])
    
    if response.status_code >= 400:
        logging.error(f"Ответ от сервера: {response.status_code} {response.body}")
    else:
        logging.info(f"Ответ от сервера: {response.status_code} {response.body}")
    
    # Проверяем смогли ли мы подключиться к серверу и получить ответ
    if response == -1:
        print("Не удалось подключиться к серверу")
    else:
        print(f"Код ответа: {response.status_code}\nТело ответа: {response.body}")


if __name__ == "__main__":
    main()
