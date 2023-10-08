import requests
from constants import API_HOST, API_PORT
from logger_config import logger


def get_address(resource):
    return f"http://{API_PORT}:{API_HOST}/{resource}"


def fetch_data(url, params=None):
    with requests.Session() as s:
        resp = s.get(url, params=params)
        if resp.status_code != 200:
            logger.warning(f"Не удалось получить данные из {url}. Status code: {resp.status_code}")
            return []
        return resp.json().get("data", [])
