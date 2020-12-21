import pandas as pd
import json
import numpy as np
import plotly.express as px

if __name__ == "__main__":
    with open("data/json/fcc_counties.json") as jfile:
        fcc = json.load(jfile)
    # Get the median value of download and upload broadband speed in each county in fcc_counties
    # fcc_median[key] = [median_download_speed, median_upload_speed]
    fcc_median = {key : fcc[key][1] for key in fcc}

    with open("data/json/acs_counties.json") as jfile:
        acs = json.load(jfile)
    # Get the population, and school age population
    # acs_pop[key] = [population, number of students]
    acs_pop = {key: [acs[key][0], acs[key][1]] for key in acs}

    # find the total population and the number of students
    total_pop, total_students = np.sum(list(acs_pop.values()), axis=0)
    print("Population Values\n\tTotal US Population: %s\n\tTotal US Students: %s" %(total_pop, total_students))

    # the first bucket is where the upload and download speed is less than 1 mbps
    bucket1_pop, bucket1_student = 0, 0
    # the second bucket is where upload and download speed is less than 2 mbps
    bucket2_pop, bucket2_student = 0, 0
    # the third bucket is where the upload speed is < 2 or the download speed < 5
    bucket3_pop, bucket3_student = 0, 0
    # the fourth bucket is where the upload speed >2 and download speed >5.
    bucket4_pop, bucket4_student = 0, 0

    for key in acs_pop:
        download, upload = fcc_median[key]
        county_pop, county_students = acs_pop[key]

        if upload >= 2.0 and download >= 5.0:
            bucket1_pop += county_pop
            bucket1_student += county_students
        elif upload >= 2.0 and download >= 2.0:
            bucket2_pop += county_pop
            bucket2_student += county_students
        elif upload >= 1.0 and download >= 1.0:
            bucket3_pop += county_pop
            bucket3_student += county_students
        else:
            bucket4_pop += county_pop
            bucket4_student += county_students

    print("RESULTS 1: Total")
    print("\tBUCKET 1: %s\t%s" % (bucket1_pop, bucket1_student))
    print("\tBUCKET 2: %s\t%s" % (bucket2_pop, bucket2_student))
    print("\tBUCKET 3: %s\t%s" % (bucket3_pop, bucket3_student))
    print("\tBUCKET 4: %s\t%s" % (bucket4_pop, bucket4_student))

    print("RESULTS 1: Percentage")
    print("\tBUCKET 1: %s\t%s" % (bucket1_pop / total_pop, bucket1_student / total_students))
    print("\tBUCKET 2: %s\t%s" % (bucket2_pop / total_pop, bucket2_student / total_students))
    print("\tBUCKET 3: %s\t%s" % (bucket3_pop / total_pop, bucket3_student / total_students))
    print("\tBUCKET 4: %s\t%s" % (bucket4_pop / total_pop, bucket4_student / total_students))

    # Load the counties geojson file
    with open("data/json/heatmap_counties.json") as jfile:
        counties = json.load(jfile)

    keys, speed = [], []
    for key in fcc:
        keys.append(key)
        if fcc_median[key][1] < 2.:
            speed.append("Slow")
        elif fcc_median[key][1] >= 3. and fcc_median[key][0] >= 25.:
            speed.append("Fast")
        else:
            speed.append("Acceptable")
    df = pd.DataFrame({'counties': keys, 'speed': speed})

    fig = px.choropleth(df, geojson=counties, locations='counties', color='speed',
                        color_discrete_sequence=['green', 'red', 'yellow'],
                        scope="usa",
                        title='Broadband Speed in US Counties'
                        )
    fig.write_image("figures/SpeedHeatmap.png")
    fig.show()
