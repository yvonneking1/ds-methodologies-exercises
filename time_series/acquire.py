import pandas as pd

#to make HTTP requests
import requests


def get_items():
    response = requests.get('https://python.zach.lol/api/v1/items')
    data = response.json()
    
    first_page_of_items = data["payload"]["items"]
    
    url_for_second_page = data["payload"]["next_page"]
    response = requests.get("https://python.zach.lol" + url_for_second_page)
    second_page_of_items = data["payload"]["items"]
    
    url_for_third_page = data["payload"]["next_page"]
    response = requests.get("https://python.zach.lol" + url_for_third_page)
    third_page_of_items = data["payload"]["items"]
    
    items = []
    items = first_page_of_items + second_page_of_items + third_page_of_items
    items = pd.DataFrame(items)
    
    return items


def get_store_data():
    response = requests.get('https://python.zach.lol/api/v1/stores')
    data = response.json()
    first_page_of_stores = data["payload"]["stores"]
    stores = pd.DataFrame(first_page_of_stores)
    return stores



def get_sale_data_from_api():
    BASE_URL = 'https://python.zach.lol'
    API_BASE = BASE_URL + '/api/v1'
    
    url = API_BASE + '/sales'
    response = requests.get(url)
    data = response.json()
    
    sales = data['payload']['sales']

    while data['payload']['next_page'] is not None:
        print('On page {} of {}'.format(data['payload']['page'] + 1, data['payload']['max_page']))
        url = BASE_URL + data['payload']['next_page']
        response = requests.get(url)
        data = response.json()
        sales += data['payload']['sales']

    return pd.DataFrame(sales)


def get_all_data():
    sales = pd.read_csv('sales.csv')
    sales = sales.rename(columns={"item": "item_id", "store": "store_id"})
    items = get_items()
    stores = get_store_data()
    
    df = sales.merge(items, on="item_id").merge(stores, on="store_id")
    
    return df
    