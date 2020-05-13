import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#to make HTTP requests
import requests

import acquire



def prep_store_data():
    #get the data from acquire file
    store = acquire.get_all_data()
    
    #Add a 'month' and 'day of week' column
    store["month"] = store.index.month_name()
    store["day_of_week"] = store.index.day_name()
    
    #Add sales total column from sale_amount and item_price
    store["sales_total"] = store.sale_amount * store.item_price
    
    #new column that is the result of the current sales - the previous days sales.
    store["sales_diff(1)"] = store.sales_total.diff(1)
    
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
    
    return ops