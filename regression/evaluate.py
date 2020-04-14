import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydataset
%matplotlib inline


from sklearn.metrics import mean_squared_error
from math import sqrt

from statsmodels.formula.api import ols

import split_scale


def plot_residuals_simple_1(y, yhat, color="tab:cyan"):
    residuals = y - yhat
    plt.scatter(y, residuals, color=color)
    return plt.gca

def regression_errors(y, yhat):
    """
    Takes in two columns: y - actual values, and yhat - predictions
    returns 5 values in this order:
    sum of squared errors (SSE)
    explained sum of squares (ESS)
    total sum of squares (TSS)
    mean squared error (MSE)
    root mean squared error (RMSE)
    """
    SSE = mean_squared_error(y, yhat)*len(y)
    ESS = sum((yhat - y.mean())**2)
    TSS = ESS + SSE
    MSE = mean_squared_error(y, yhat)
    RMSE = sgrt(MSE)
    return SSE, ESS, TSS, MSE, RMSE

def baseline_mean_errors(y):
    """
    Takes in one column: y - actual values
    Returns 3 baseline values in this oder:
    sum of squared errors (SSE)
    mean squared error (MSE)
    root mean squared error (RMSE)
    """
    SSE = mean_squared_error(y, y.mean())*len(y)
    MSE = mean_squared_error(y, y.mean())
    RMSE = sqrt(MSE)
    return SSE, MSE, RMSE

def better_than_baseline(y, yhat):
    """
    Takes in two columns: y - actual values, and yhat - predictions
    Returns True if model is performing better than the baseline.
    Our baseline in this function is the mean of y
    """
    SSE = mean_squared_error(y, yhat)*len(y)
    SSE_baseline = mean_squared_error(y, y.mean())*len(y)
    if SSE > SSE_baseline:
        return True
    else:
        return False
    
def model_significance(ols_model):
    r2 = ols_model.rsquared
    f_pvalue = ols_model.f_pvalue
    return "p-value = ", f_pvalue, "R-Squared = ", r2

def plot_residuals_simple(actual, predicted):
    residuals = actual - predicted
    plt.hlines(0, actual.min(), actual.max(), ls=':')
    plt.scatter(actual, residuals)
    plt.ylabel('residual ($y - \hat{y}$)')
    plt.xlabel('actual value ($y$)')
    plt.title('Actual vs Residual')
    return plt.gca()