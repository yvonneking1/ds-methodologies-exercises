import pandas as pd


def get_titanic_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1PmmRUXgmQ6oO9fLORG4oeMLe_mzIWlFAkJKA2cwLOLg/edit#gid=935554057"
    csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df_titanic = pd.read_csv(csv_export_url)
    return df_titanic