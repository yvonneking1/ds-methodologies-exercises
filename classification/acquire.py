import pandas as pd
import env

def get_db_url(db):
    return f'mysql+pymysql://{env.user}:{env.password}@{env.host}/{db}'


def get_titanic_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1PmmRUXgmQ6oO9fLORG4oeMLe_mzIWlFAkJKA2cwLOLg/edit#gid=935554057"
    csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df_titanic = pd.read_csv(csv_export_url)
    return df_titanic


def get_iris_data():
    url = get_db_url("iris_db")
    query = """SELECT * 
    FROM measurements
    JOIN species USING(species_id);"""
    df = pd.read_sql(query, url)
    return df