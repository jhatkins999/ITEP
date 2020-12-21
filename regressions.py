import pandas as pd
import json
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt

import statsmodels.api as sm

if __name__ == "__main__":
    # This function is needed to sort out n/a values from cost
    def isFloat(string):
        try:
            float(string)
            return True
        except ValueError:
            return False


    with open("data/json/fcc_counties.json") as jfile:
        fcc = json.load(jfile)
    # Get the median value of download and upload broadband speed in each county in fcc_counties
    # fcc_median[key] = [median_download_speed, median_upload_speed]
    fcc_median = {key : fcc[key][1] for key in fcc}

    with open("data/json/urban_counties.json") as jfile:
        urban_data = json.load(jfile)

    urban = {key : int(urban_data[key] >= 1) for key in urban_data}

    with open("data/json/cost_counties.json") as jfile:
        cost_data = json.load(jfile)
    # cost data contains percent broaband, number of options, and the lowest cost plan
    cost = {key : float(cost_data[key][2]) for key in cost_data if isFloat(cost_data[key][2])}
    # Calculate the mean and standard deviation of the cost data to normalize it
    cost_std = np.std(list(cost.values()))
    cost_mean = np.mean(list(cost.values()))

    normalized_cost = {key: (cost[key] - cost_mean) / cost_std for key in cost}

    df_dict = {"NormalizedCost" : [], "MedianCountySpeed" : [], "isMetroCounty" : []}
    # collect all the data for the regression into a dict
    for key in normalized_cost:
        df_dict["NormalizedCost"].append(normalized_cost[key])
        df_dict["MedianCountySpeed"].append(int(fcc_median[key][1] >= 2.))
        df_dict["isMetroCounty"].append(urban[key])
    # turn the dict into a datafram
    reg_df = pd.DataFrame(df_dict)
    print(reg_df.head)
    results = sm.Logit(reg_df['MedianCountySpeed'], reg_df[['NormalizedCost', 'isMetroCounty']]).fit()
    print(results.summary())