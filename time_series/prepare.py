import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#to make HTTP requests
import requests

import acquire


def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    plt.rc('figure', figsize=(11, 9))
    plt.rc('font', size=13)
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='thistle')
    plt.suptitle('Numeric Column Distributions')
    plt.show()
    

def prep_store_data():
    #get the data from acquire file
    store = acquire.get_all_data()
    
    #Add a 'month' and 'day of week' column
    store["month"] = store.index.month_name()
    store["weekday"] = store.index.day_name()
    
    #Add sales total column from sale_amount and item_price
    store["sales_total"] = store.sale_amount * store.item_price
    
    #new column that is the result of the current sales - the previous days sales.
    store["sales_diff(1)"] = store.sales_total.diff(1)
    
    # Change dtypes of numeric columns to object and category
    store = (store.astype({'sale_id': object, 'store_id': object, 
                     'store_zipcode': object, 'item_id': object, 
                     'item_upc12': object, 'item_upc14': object, 
                     'month': 'category', 'weekday': 'category'}))
    
    numeric_hists(store)
    
    return store


def prep_german_energy():
    #get the data from acquire file
    ops = acquire.german_energy_csv()
    
    # Convert date column to datetime format.
    ops["Date"] = pd.to_datetime(ops["Date"])
    
    # Set the index to be the datetime variable.
    ops = ops.sort_values("Date").set_index("Date")
    
    #Add a month and a year column
    ops["month"] = ops.index.month_name()
    ops["year"] = ops.index.year
   
    
    numeric_hists(ops)
    
    return ops