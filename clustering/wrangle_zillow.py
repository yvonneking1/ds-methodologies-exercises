
# Wrangling
import pandas as pd
import numpy as np

# Exploring
import scipy.stats as stats

# default pandas decimal number display format
pd.options.display.float_format = '{:20,.2f}'.format

from env import get_db_url


def get_zillow_data():
    url = get_db_url("zillow")

    sql = """
    SELECT
    Z.parcelid,
    Z.basementsqft,
    Z.bathroomcnt,
    Z.bedroomcnt,
    Z.calculatedbathnbr,
    Z.finishedfloor1squarefeet,
    Z.calculatedfinishedsquarefeet,
    Z.finishedsquarefeet12,
    Z.finishedsquarefeet13,
    Z.finishedsquarefeet15,
    Z.finishedsquarefeet50,
    Z.finishedsquarefeet6,
    Z.fips,
    Z.fireplacecnt,
    Z.fullbathcnt,
    Z.garagecarcnt,
    Z.garagetotalsqft,
    Z.hashottuborspa,
    Z.latitude,
    Z.longitude,
    Z.lotsizesquarefeet,
    Z.poolcnt,
    Z.poolsizesum,
    Z.propertycountylandusecode,
    Z.propertyzoningdesc,
    Z.regionidcity,
    Z.regionidcounty,
    Z.regionidneighborhood,
    Z.regionidzip,
    Z.roomcnt,
    Z.threequarterbathnbr,
    Z.unitcnt,
    Z.yardbuildingsqft17,
    Z.yardbuildingsqft26,
    Z.yearbuilt,
    Z.numberofstories,
    Z.fireplaceflag,
    Z.structuretaxvaluedollarcnt,
    Z.taxvaluedollarcnt,
    Z.assessmentyear,
    Z.landtaxvaluedollarcnt,
    Z.taxamount,
    Z.taxdelinquencyflag,
    Z.taxdelinquencyyear,
    Z.censustractandblock,
    unique_properties.logerror,
    unique_properties.transactiondate,
    plt.propertylandusedesc,
    st.storydesc,
    ct.typeconstructiondesc,
    act.airconditioningdesc,
    bct.buildingclassdesc,
    hst.heatingorsystemdesc
    FROM 
    (SELECT 
    p17.parcelid,
    logerror,
    transactiondate
    FROM 
    predictions_2017 AS p17
    JOIN
    (SELECT 
    predictions_2017.parcelid,
    MAX(transactiondate) AS max_trans_date
    FROM predictions_2017
    GROUP BY predictions_2017.parcelid) AS pred_agg ON (p17.parcelid=pred_agg.parcelid) AND (pred_agg.max_trans_date=p17.transactiondate)) AS unique_properties
    LEFT JOIN properties_2017 AS Z ON (Z.parcelid=unique_properties.parcelid)
    LEFT JOIN propertylandusetype AS plt ON (Z.propertylandusetypeid=plt.propertylandusetypeid)
    LEFT JOIN storytype AS st ON (Z.storytypeid=st.storytypeid)
    LEFT JOIN typeconstructiontype AS ct ON (Z.typeconstructiontypeid=ct.typeconstructiontypeid)
    LEFT JOIN airconditioningtype AS act ON (Z.airconditioningtypeid=act.airconditioningtypeid)
    LEFT JOIN architecturalstyletype AS ast ON (Z.architecturalstyletypeid=ast.architecturalstyletypeid)
    LEFT JOIN buildingclasstype AS bct ON (Z.buildingclasstypeid=bct.buildingclasstypeid)
    LEFT JOIN heatingorsystemtype AS hst ON (Z.heatingorsystemtypeid=hst.heatingorsystemtypeid)
    WHERE Z.latitude IS NOT NULL AND Z.longitude IS NOT NULL
    """
    df = pd.read_sql(sql, url)
    return df

def df_summary(df):
    print("---Shape:",df.shape)
    print("---Info")
    print(df.info())
    print("---Describe")
    print(df.describe())

def nulls_by_column(df):
    """
    Returns a dataframe that tells you how many rows are null and the percentage that is missing in that column
    """
    attributes = pd.DataFrame({"num_rows_missing": df.isnull().sum(), "pct_row_missing": df.isna().sum()/len(df)}, index=df.columns)
    return attributes

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing 

def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df

def label_county(row):
    if row['fips'] == 6037:
        return 'Los Angeles'
    elif row['fips'] == 6059:
        return 'Orange'
    elif row['fips'] == 6111:
        return 'Ventura'


def prep_zillow(cols_to_remove=['calculatedbathnbr', 'regionidneighborhood'], prop_required_column=.5, prop_required_row=.75):
    zillow = get_zillow_data()
    
    #insure that this is a single unit property
    zillow = zillow[zillow.propertylandusedesc.isin(["Single Family Residential", "Residential General"])]
    zillow = zillow[(zillow.bedroomcnt > 0) & (zillow.bathroomcnt > 0)]
    zillow = remove_columns(zillow, cols_to_remove)
    zillow = handle_missing_values(zillow, prop_required_column, prop_required_row)
    
    # Set nulls to specific value
    zillow.calculatedfinishedsquarefeet[zillow.calculatedfinishedsquarefeet.isna()] = zillow.calculatedfinishedsquarefeet.median()
    
    zillow.finishedsquarefeet12 = zillow.finishedsquarefeet12.fillna(1456.0)
    
    zillow.lotsizesquarefeet = zillow.lotsizesquarefeet.fillna(zillow.lotsizesquarefeet.median())
    
    zillow = zillow.dropna(subset=['regionidcity', 'regionidzip', 'censustractandblock'])
    
    zillow.propertyzoningdesc = zillow.propertyzoningdesc.fillna('LAR1')
    
    zillow.heatingorsystemdesc = zillow.propertyzoningdesc.fillna('N/A')
    
    zillow.structuretaxvaluedollarcnt = zillow.structuretaxvaluedollarcnt.fillna(zillow.structuretaxvaluedollarcnt.median())
    
    zillow.yearbuilt = zillow.yearbuilt.fillna(zillow.yearbuilt.median())
    
    zillow.taxamount = zillow.taxamount.fillna(zillow.taxamount.median())
    
    zillow.unitcnt = zillow.unitcnt.fillna(1.0)
    
    zillow['County'] = zillow.apply(lambda row: label_county(row), axis=1)

    zillow['State'] = 'CA'
    
    zillow = zillow.dropna(axis=1)
    
    return zillow