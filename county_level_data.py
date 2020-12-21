# This file will load the fcc, acs and cost data and output the county level data of each
# The three files will have common keys after this file runs
# The files will be kept as json files in data/json

import pandas as pd
from collections import defaultdict
import json

# Get the county codes from the fcc_acc_merged data
# The county code is the first 5 digits of the fips code

acs_data = pd.read_csv("data/acs2.csv")
cost = pd.read_csv("data/broadband_data_bbn.csv")

# Initialize empty dictionaries to store the county level data
fcc_counties = defaultdict(list)
acs_counties = defaultdict(list)
county_cost = {}
# Take the download and uploade speed from the fcc data : cols 4 and 5
with open("data/json/merged_fcc_data.json") as jsonfile:
    fcc_data = json.load(jsonfile)

# Take the population, school age population, households with computers, households with broadband, number of households
# from the acs data cols 1, 7+11+15, 19, 23, 3
for i, j in acs_data.iterrows():
    values = j.values
    acs_counties[str(values[0])[:5]].append([values[1], values[7]+values[11]+values[15], values[19], values[23], values[3]])
with open("data/json/acs_counties.json", "w") as jsonfile:
    json.dump(acs_counties, jsonfile, indent=4)
# Take the percentage of households with broadband, number of providers, cost cols 3, 5, 9
for i, j in cost.iterrows():
    values = j.values
    key = str(values[1])
    # Add an extra zero if it isnt long enough to ensure the keys are the same for each dict
    if len(key) == 4:
        key = '0'+key
    county_cost[key] = [values[3], values[5], values[9]]
with open("data/json/county_cost.json", "w") as jsonfile:
    json.dump(county_cost, jsonfile, indent=4)

count1 = 0
count2 = 0
count3 = 0
for key in fcc_counties:
    if key in county_cost:
        count1 +=1
    if key in acs_counties:
        count3 += 1
for key in acs_counties:
    if key in county_cost:
        count2 += 1

print(count1, count2, count3)