# -*- coding: utf-8 -*-
"""
Created on Thu May  4 01:48:16 2023

@author: johode
"""


# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import expon
import json
import pandas as pd
import datetime
import reliability

start_date = datetime.datetime(2000, 1, 1)
end_date = datetime.datetime(2020, 12, 31)

# Write the JSON file
with open('hydropower_work_orders.json') as file:
    work_orders = json.load(file)

df = pd.DataFrame([order for order in work_orders if order['type'] in ['ACM', 'DCM']])

for col in df.columns:
    if 'date_' in col:
        df[col] = pd.to_datetime(df[col])

# Use date reported as event and set component as index
failure_times = df.set_index('component')['date_reported']

# Compute time betwen failures for each component
time_between_failures = failure_times.groupby(level=0).diff()

# First failure, failure time is relative start date (left censored)
time_between_failures.loc[time_between_failures.isna()] = failure_times.groupby(level=0).min()-start_date
# time_between_failures.fillna(failure_times.groupby(level=0).min()-start_date)

for component in time_between_failures.index.unique():
    tbf_days = time_between_failures.loc[component].values*1e-9/(60*60*24)
    # Fit exponential distribution for CM actions
    result = reliability.Fitters.Fit_Exponential_1P(
        failures=tbf_days,
        show_probability_plot=False, 
        print_results=False)
    
    print(f"{component}: lam={result.Lambda:.4f}")
