import requests
import os
import logging
from datetime import date, timedelta
from celery import shared_task

from ml.model import forecast

URL_CATEGORIES = "api/v1/categories"
URL_SALES = "api/v1/sales"
URL_STORES = "api/v1/shops"
URL_FORECAST = "api/v1/forecast"

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
        _logger.warning("Could not get stores list")
        return []
    return resp.json()["data"]


def get_categories():
    categs_url = get_address(URL_CATEGORIES)
    resp = requests.get(categs_url)
    if resp.status_code != 200:
        _logger.warning("Could not get category info")
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
        _logger.warning("Could not get sales history")
        return []
    return resp.json()

@shared_task
def main(today=date.today()):
    forecast_dates = [today + timedelta(days=d) for d in range(1, 6)]
    forecast_dates_str = [el.strftime("%Y-%m-%d") for el in forecast_dates]
    categs_info = get_categories()

    for store in get_stores():
        result = []

        for item in get_sales(store=store["store"]):
            item_info = categs_info[item["sku"]]
            sales = item.get("fact")
            
            if sales is None:
                # Обработка ситуации, когда sales равен None
                print(f"Warning: No sales data for item {item.get('sku')}, store {store['store']}")
                continue
            
            sales_dict = {
                "date": sales.get("date"),
                "sales_type": sales.get("sales_type", 0),
                "sales_units": sales.get("sales_units", 0),
                "sales_units_promo": sales.get("sales_units_promo", 0), 
                "sales_rub": float(sales.get("sales_rub", "0")),  
                "sales_rub_promo": float(sales.get("sales_rub_promo", "0")),  
            }

            print(f'Магазин: {store}') # Принт данных из базы по магазин
            print(f'Продажи: {sales_dict}') #Принт данных из базы по продажам
            
            print(f'Айтемы: {item_info}') #Принт данных из базы по позицияи
            
            
        #     prediction = forecast(sales=sales_dict, item_info=item_info, store_info=store)

        #     result.append({
        #         "store": store["store"],
        #         "sku": item["sku"],
        #         "forecast_date": today.strftime("%Y-%m-%d"),
        #         "sales_units": [
        #             {"date": date, "target": target} for date, target in zip(forecast_dates_str, prediction)
        #             ]
        #         })
        
        # requests.post(get_address(URL_FORECAST), json={"data": result})


if __name__ == "__main__":
    setup_logging()
    main()
