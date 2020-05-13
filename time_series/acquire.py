import pandas as pd
import os

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
    

    #checks to see if the dataframe is a CSV
    if os.path.isfile('big_df.csv'):
        df = pd.read_csv('big_df.csv', parse_dates=True, index_col='sale_date')
        return df
    else:
        # convert sale_date to DateTime Index
        df['sale_date'] = pd.to_datetime(df.sale_date)
        df = df.sort_index()# convert sale_date to DateTime Index
        df['sale_date'] = pd.to_datetime(df.sale_date)
        df = df.sort_index()
        
        #write to csv for future use
        df.to_csv('big_df.csv')
        return df    

    
def german_energy_csv():
    """
    This function returns a df with a datetime index
    using the opsd_germany url/csv.
    """
    if os.path.isfile('german_energy.csv'):
        df = pd.read_csv('german_energy.csv')
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df.to_csv('german_energy.csv')
    return df  