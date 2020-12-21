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

    with open("data/json/cost_counties.json") as jfile:
        cost_data = json.load(jfile)
    # cost data contains percent broaband, number of options, and the lowest cost plan
    cost = {key : float(cost_data[key][2]) for key in cost_data if isFloat(cost_data[key][2])}
    # Calculate the mean and standard deviation of the cost data to normalize it
    cost_std = np.std(list(cost.values()))
    cost_mean = np.mean(list(cost.values()))

    normalized_cost = {key : (cost[key] - cost_mean) / cost_std for key in cost}

    # Collect the normalized cost as the independant variable and speed as the dependant
    X, y, y_bin = [], [], []
    for key in normalized_cost:
        X.append(normalized_cost[key])
        y.append(fcc_median[key][1])
        y_bin.append(int(fcc_median[key][1] >= 2.)) # y_bin binarizes the upload speed

    # Compute the ols regression for X and y and a logit regression for X and y_bin
    results_ols = sm.OLS(y, X).fit()
    results_logit = sm.Logit(y_bin, X).fit()
    # OLS Summary
    print(results_ols.summary())
    # Logit summary
    print(results_logit.summary())

    # Plot the normalized cost vs Upload speed graph
    # plt.scatter(X, y)
    # plt.title("Upload Speed vs Normalized Cost")
    # plt.xlabel("Normalized Cost (std from the mean)")
    # plt.ylabel("Upload Speed (mbps)")
    # plt.savefig("CostVSpeed.png")
    # plt.show()

    # Load the counties geojson file
    with open("data/json/heatmap_counties.json") as jfile:
        counties = json.load(jfile)

    # Create the dataframe to pass to the heat map
    keys, cost_speed = [], []
    for key in cost:
        keys.append(key)
        if normalized_cost[key] < 1. and fcc_median[key][1] >= 2.:
            cost_speed.append("Fast and Cheap")
        elif fcc_median[key][1] >= 2:
            cost_speed.append("Fast and Expensive")
        elif normalized_cost[key] < 1.:
            cost_speed.append("Slow and Cheap")
        else:
            cost_speed.append("Slow and Expensive")

    df = pd.DataFrame({'counties': keys, 'CostSpeed' : cost_speed})


    # Generate the heatmap for cost and speed
    # Plot heat maps
    fig = px.choropleth(df, geojson=counties, locations='counties', color='CostSpeed',
                        color_discrete_sequence=['green', 'yellow', 'orange', 'red'],
                        scope="usa",
                        title='Normalized Cost of Broadband and Upload Speed in US Counties'
                        )
    fig.update_layout(legend = dict())
    fig.write_image("figures/SpeedCostHeatmap.png")
    fig.show()




