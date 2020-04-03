import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

import env
import wrangle
import split_scale

def plot_variable_pairs(dataframe):
    """This function returns a pairplot to help explore relationships"""
    return sns.pairplot(dataframe, kind="reg")

def months_to_years(tenure_months, df):
    df["tenure_years"] = tenure_months // 12
    return df

def plot_categorical_and_continous_vars(categorical_var, continuous_var, dataframe):
    """This function returns 3 plots to explore relationships
    returns: 1. nested boxplot and swarmplot. 2. violinplot 3. barplot"""
    f, axes = plt.subplots(3,1, figsize=(16,16))
    
    sns.boxplot(y=categorical_var, x=continuous_var, data=dataframe, ax=axes[0])
    sns.swarmplot(y=categorical_var, x=continuous_var, data=dataframe, color =".2", alpha=.7, ax=axes[0])
    sns.violinplot(y=categorical_var, x=continuous_var, data=dataframe, inner="stick", ax=axes[1])
    sns.barplot(y=categorical_var, x=continuous_var, data=dataframe, ax=axes[2])