import pandas as pd
import env

def get_db_url(db):
    return f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'


def get_titanic_data():
    url= get_db_url("titanic_db")
    query = "SELECT * FROM passengers"
    df = pd.read_sql(query, url)
    return df


def get_iris_data():
    url = get_db_url("iris_db")
    query = """SELECT * 
    FROM measurements
    JOIN species USING(species_id);"""
    df = pd.read_sql(query, url)
    return df