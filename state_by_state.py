import pandas as pd
import json
import numpy as np
from collections import defaultdict

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

    with open("data/json/heatmap_states.json") as jfile:
        state_codes = json.load(jfile)

    temp_urban = defaultdict(list)
    temp_speed = defaultdict(list)

    for key in urban:
        state = state_codes[key[:2]]
        temp_urban[state].append(urban[key])
        temp_speed[state].append(fcc_median[key])

    urban_states = {key : np.mean(temp_urban[key]) for key in temp_urban}
    speed_states = {key : np.mean(temp_speed[key]) for key in temp_speed}

    X, y = [], []
    for key in urban_states:
        X.append(urban_states[key])
        y.append(speed_states[key])

    m, b = np.polyfit(X, y, 1)
    print("m:", m, "b:", b)
    plt.scatter(X, y)
    plt.plot(np.array(X), m*np.array(X)+b)
    plt.title("Speed Vs Metropolitan by State")
    plt.xlabel("Percent of Counties that are Metropolitan")
    plt.ylabel("Average Upload Speed by State")
    plt.savefig("StateSpeedVUrbanState.png")
    plt.show()



