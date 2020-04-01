import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from env import get_db_url

def wrangle_telco():
    query = """SELECT customer_id,
    tenure,
    monthly_charges,
    total_charges
    FROM customers
    WHERE contract_type_id = 3;"""
    url = get_db_url("telco_churn")
    telco = pd.read_sql(query, url)
    telco.total_charges = telco.total_charges.str.strip()
    telco = telco.replace("", np.nan)
    telco = telco.dropna()
    telco.total_charges = telco.total_charges.astype("float")
    return telco