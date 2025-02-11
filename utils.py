import requests
from time import sleep
from fake_useragent import UserAgent
from loguru import logger

ua = UserAgent()


def load_sessions(file_path='sessions.txt'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def create_headers(session):
    return {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru-RU,ru;q=0.7',
        'origin': 'https://v1.jtmkbot.click',
        'priority': 'u=1, i',
        'referer': 'https://v1.jtmkbot.click/',
        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sec-gpc': '1',
        'secure-header': f"{session}",
        'user-agent': ua.random,
    }


def get_info(headers, thread_id):
    response = requests.get('https://api.jtmkbot.click/wallet/balance', headers=headers).json()
    balance = response.get('balance', 0)
    logger.success(f"Аккаунт ({thread_id}) завершил свою работу. Баланс: {balance} монеток.")


def spin(session, thread_id):
    headers = create_headers(session=session)
    logger.info(f"Аккаунт ({thread_id}) начал свою работу.")

    while True:
        try:
            response = requests.post('https://api.jtmkbot.click/roulette/spin', headers=headers)
            sleep(1)

            if '"code":1005' in response.text or "You have reached your spin limit" in response.text:
                logger.warning(f"Аккаунт ({thread_id}): Все спины закончились.")
                break
            elif response.status_code != 200:
                logger.error(f"Аккаунт ({thread_id}): Неизвестная ошибка, код: {response.status_code}")
            else:
                continue
        except requests.RequestException as e:
            logger.error(f"Аккаунт ({thread_id}): Ошибка: {e}")
            break

    get_info(headers, thread_id)
