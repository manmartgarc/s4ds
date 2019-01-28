# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 23:21:32 2019

@author:    manma
@project:   Practical Statistics for Data Science
            Chapter 1. Exploratory Data Analysis
"""
import os
import pandas as pd
import numpy as np
from scipy.stats import trim_mean

# %% initialize environment
ROOT_DIR = os.path.join(os.getcwd(), '../..')
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# %% load data
df = pd.read_csv(os.path.join(DATA_DIR, 'state.csv'))

# %% Example: Location estimates of Population and Murder Rates
# take the mean of a column
print('Population mean = {}'.format(df['Population'].mean()))

# take the trimmed mean (not the same as windsorize)
print('Population trimmed mean = {}'
      .format(trim_mean(df['Population'], proportiontocut=0.1)))

# median of a column
print('Population median = {}'.format(df['Population'].median()))

# weighted mean
"""
this will be a little bit more tricky since there are no included
weighted mean functions in pandas or numpy. To get the weights,
we can define a function that specifies a variable to get the weights,
and then another column from which we would like to get the means
"""


def wmean(group_col, mean_col, weight_col, data=df):
    """
    Take the mean of mean_col and apply the weights from weight_col
    and returns a weighted mean
    """
    # calculate weights
    weights = \
        data.groupby(group_col)[weight_col].sum() / data[weight_col].sum()

    # calculate means
    means = \
        data.groupby(group_col)[mean_col].mean()

    # concatenate to make sure weight_i is with mean_i
    x = pd.concat([weights, means], axis=1)

    # muliply weights * means, and divide over the sum of the weights.
    w_mean = x.prod(axis=1).sum() / weights.sum()

    return w_mean


print('Weighted mean = {}'
      .format(wmean(group_col='State',
                    mean_col='Murder.Rate',
                    weight_col='Population',
                    data=df)))

# unweighted mean
print('Unweighted mean = {}'.format(df['Murder.Rate'].mean()))
