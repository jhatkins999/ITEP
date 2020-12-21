import pandas as pd
import json
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt

import statsmodels.api as sm

if __name__ == "__main__":
    with open("data/json/fcc_counties.json") as jfile:
        fcc = json.load(jfile)
    # Get the median value of download and upload broadband speed in each county in fcc_counties
    # fcc_median[key] = [median_download_speed, median_upload_speed]
    fcc_median = {key : fcc[key][1] for key in fcc}

    with open("data/json/urban_counties.json") as jfile:
        urban_data = json.load(jfile)

    urban = {key : int(urban_data[key] >= 1) for key in urban_data}

    X, y, y_bin = [], [], []
    for key in urban:
        X.append(urban[key])
        y.append(fcc_median[key][1])
        y_bin.append(int(fcc_median[key][1] >= 2.))  # y_bin binarizes the upload speed


    results_ols = sm.OLS(y, X).fit()
    results_logit = sm.Logit(y_bin, X).fit()
    # OLS Summary
    print(results_ols.summary())
    # Logit summary
    print(results_logit.summary())

    # Plot the normalized cost vs Upload speed graph
    plt.scatter(X, y)
    plt.title("Upload Speed vs Metropolitan Areas")
    plt.xlabel("Metropolitan Area")
    plt.ylabel("Upload Speed (mbps)")
    plt.savefig("UrbanVSpeed.png")
    plt.show()

    # Load the counties geojson file
    with open("data/json/heatmap_counties.json") as jfile:
        counties = json.load(jfile)

    # Create the dataframe to pass to the heat map
    keys, urban_speed = [], []
    # for key in urban:
    #     keys.append(key)
    #     if urban[key] == 1 and fcc_median[key][1] >= 2.:
    #         urban_speed.append("Metropolitan and Fast")
    #     elif fcc_median[key][1] >= 2:
    #         urban_speed.append("Non-Metropolitan and Fast")
    #     elif urban[key] == 1:
    #         urban_speed.append("Metropolitan and Slow")
    #     else:
    #         urban_speed.append("Non-Metropolitan and Slow")
    #
    # df = pd.DataFrame({'counties': keys, 'UrbanSpeed' : urban_speed})
    #
    #
    # # Generate the heatmap for cost and speed
    # # Plot heat maps
    # fig = px.choropleth(df, geojson=counties, locations='counties', color='UrbanSpeed',
    #                     color_discrete_sequence=['green', 'yellow', 'orange', 'red'],
    #                     scope="usa",
    #                     title='Metropolitan Counties and Upload Speed in the US'
    #                     )
    # fig.update_layout(legend = dict())
    # fig.write_image("figures/UrbanSpeedHeatmap.png")
    # fig.show()

