import pandas as pd
import numpy as np
import acquire

import matplotlib.pyplot as plt
import seaborn as sns

import sklearn.model_selection
import sklearn.impute
import sklearn.preprocessing

import warnings
warnings.filterwarnings("ignore")

import acquire

def drop_columns(df):
    return df.drop(columns=["species_id", "measurement_id"])

def rename_species_column_name(df):
    return df.rename(columns={"species_name": "species"})

def label_encode(train, test):
    le = sklearn.preprocessing.LabelEncoder()
    train['species'] = le.fit_transform(train.species)
    test['species'] = le.transform(test.species)
    return le, train, test


def prep_iris(df):
    df = drop_columns(df)
    df = rename_species_column_name(df)
    train, test = sklearn.model_selection.train_test_split(df, train_size=.8, random_state=123)
    train, test = label_encode(train, test)
    return le, train, test

def inverse_encode(train, test, le):
    train['species'] = le.inverse_transform(train.species)
    test['species'] = le.inverse_transform(test.species)
    return train, test



def drop_deck_column(df):
    return df.drop(columns=["deck"])


def impute_embark_town(train, test):
    train.embark_town = train.embark_town.fillna('Southampton')
    test.embark_town = test.embark_town.fillna('Southampton')
    return train, test


def impute_age(train, test):
    avg_age = train.age.mean()
    train.age = train.age.fillna(avg_age)
    test.age = test.age.fillna(avg_age)
    return train, test


def encode_embark_town(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder()
    encoder.fit(train[['embark_town']])
    # nice columns for display
    cols = ['embark_town_' + c for c in encoder.categories_[0]]

    m = encoder.transform(train[['embark_town']]).todense()
    train = pd.concat([
        train,
        pd.DataFrame(m, columns=cols, index=train.index)
    ], axis=1).drop(columns='embark_town')
    
    m = encoder.transform(test[['embark_town']]).todense()
    test = pd.concat([
        test,
        pd.DataFrame(m, columns=cols, index=test.index)
    ], axis=1).drop(columns='embark_town')

    return encoder, train, test



def impute_age(train, test):
    imputer = sklearn.impute.SimpleImputer(strategy='mean')
    imputer.fit(train[['age']])
    train["age_imputed"] = imputer.transform(train[['age']])
    test["age_imputed"] = imputer.transform(test[['age']])
    return train, test


def scale_minmax_for_age_and_fare(train, test, column_list = ['age_imputed','fare']):
    scaler = sklearn.preprocessing.MinMaxScaler()
    column_list_scaled = [col + '_scaled' for col in column_list]
    train_scaled = pd.DataFrame(scaler.fit_transform(train[column_list]), 
                                columns = column_list_scaled, 
                                index = train.index)
    train = train.join(train_scaled)

    test_scaled = pd.DataFrame(scaler.transform(test[column_list]), 
                                columns = column_list_scaled, 
                                index = test.index)
    test = test.join(test_scaled)

    return scaler, train, test


def prep_titanic(df):
    df = drop_deck_column(df)
    train, test = sklearn.model_selection.train_test_split(df, train_size=.75, random_state=123)
    train, test = impute_embark_town(train, test)
    train, test = impute_age(train, test)
    encoder, train, test = encode_embark_town(train, test)
    scaler, train, test = scale_minmax_for_age_and_fare(train, test, column_list = ['age_imputed','fare'])
    return scaler, encoder, train, test