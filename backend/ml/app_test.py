import requests
import os
import logging
from datetime import date, timedelta

from model import forecast

URL_CATEGORIES = "api/v1/categories"
URL_SALES = "api/v1/sales"
URL_STORES = "api/v1/shops"
URL_FORECAST = "api/v1/forecast/"

api_port = os.environ.get("API_PORT", "80")
api_host = os.environ.get("API_PORT", "94.131.100.195")

#94.131.100.195

_logger = logging.getLogger(__name__)


def setup_logging():
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)
    handler_m = logging.StreamHandler()
    formatter_m = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    handler_m.setFormatter(formatter_m)
    _logger.addHandler(handler_m)


def get_address(resource):
    return "http://" + api_host + ":" + api_port + "/" + resource


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


def main(today=date.today()):
    _logger.info(f"Запуск основного процесса с указанием даты начала: {today}")
    forecast_dates = [today + timedelta(days=d) for d in range(1, 15)]
    forecast_dates_str = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    
    _logger.info("Получение информации о категориях...")
    categs_info = get_categories()
    
    for store in get_stores():
        _logger.info(f"Обработка магазинов: {store['store']}...")
        result = []

        for item in get_sales(store=store["store"]):
            _logger.debug(f"Обработка товара: {item['sku']} для магазина: {store['store']}...")
            item_info = categs_info.get(item["sku"])
            
            if item_info is None:
                _logger.warning(f"Нет информации о категории для элемента {item['sku']} в магазине {store['store']}")
                continue

            sales = item.get("fact")
            if sales is None:
                _logger.warning(f"Отсутствие данных о продажах для товара {item['sku']}, магазин {store['store']}")
                continue
            
            _logger.debug(f"Прогнозирование для {item['sku']}...")
            prediction = forecast(sales=sales, item_info=item_info, store_info=store)

            result.append({
                "store": store["store"],
                "sku": item["sku"],
                "forecast_date": today.strftime("%Y-%m-%d"),
                "sales_units": [
                    {"date": date, "target": round(target)} for date, target in zip(forecast_dates_str, prediction)
                ]
            })
        if result:
            for r in result:
                _logger.debug(f"Отправка прогноза для магазина: {store['store']}, SKU {r['sku']} to the API...")
                response = requests.post(get_address(URL_FORECAST), json=r, headers={'Content-Type': 'application/json'})
                
                if response.status_code == 201:
                    _logger.info("Данные успешно отправлены!")
                else:
                    _logger.error(f"Не удалось отправить данные! Код состояния: {response.status_code}, Response text: {response.text}")
        else:
            _logger.warning(f"Нет данных для передачи в магазин {store['store']}")



if __name__ == "__main__":
    setup_logging()
    main()
