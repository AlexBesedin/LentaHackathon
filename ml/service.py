# import requests

# URL_CATEGORIES = "categories"
# URL_SALES = "sales"
# URL_STORES = "shops"
# URL_FORECAST = "forecast"

# api_port = "8000"
# api_host = "94.131.100.195"

# def get_address(resource):
#     return "http://94.131.100.195/api/v1/" + resource 


# def get_stores():
#     stores_url = get_address(URL_STORES)
#     resp = requests.get(stores_url)
#     if resp.status_code != 200:
#         return []
#     return resp.json()["data"]

# if __name__ == "__main__":
#     stores = get_stores()
#     print(stores)