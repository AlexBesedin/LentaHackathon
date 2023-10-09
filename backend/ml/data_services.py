import requests

from ml.constants import (API_HOST, API_PORT, URL_CATEGORIES, URL_SALES,
                          URL_STORES)
from ml.logger_config import _logger


def get_address(resource):
    return f"http://{API_HOST}:{API_PORT}/{resource}"


def get_stores():
    stores_url = get_address(URL_STORES)
    resp = requests.get(stores_url)
    if resp.status_code != 200:
        _logger.warning("Не удалось получить список магазинов")
        return []
    return resp.json()


def get_categories():
    categs_url = get_address(URL_CATEGORIES)
    resp = requests.get(categs_url)
    if resp.status_code != 200:
        _logger.warning("Не удалось получить информацию о категории")
        return {}
    result = {el["sku"]: el for el in resp.json()}
    return result


def get_sales(store=None, sku=None):
    sale_url = get_address(URL_SALES)
    params = {}
    if store is not None:
        params["store"] = store
    if sku is not None:
        params["sku"] = sku
    resp = requests.get(sale_url, params=params)
    if resp.status_code != 200:
        _logger.warning("Не удается получить историю продаж")
        return []
    return resp.json()