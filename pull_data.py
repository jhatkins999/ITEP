import csv
import numpy as np
from collections import defaultdict

# fcc_file = "data/speed_by_FIPS.csv"
fcc_file = "data/fcc_merged.csv"
acs_file = "data/ACS US - All/ACS_data.csv"
fcc_out = "data/fcc2.csv"
acs_out = "data/acs.csv"

if __name__ == "__main__":
    with open(fcc_file) as csvread:
        reader = csv.reader(csvread)
        header = True
        data = defaultdict(list)
        count = 0
        for row in reader:
            if header:
                header = False
                labels = row
                continue
            data[row[0]].append([row[1], row[2], row[3:]])
            if count % 100000 == 0:
                print("%s rows loaded" %count)
            count += 1
    print(len(data.keys()))
    print(labels)
    with open(fcc_out, "w") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(labels)
        for key in data:
            row = []
            row.append(key)
            row.append(data[key][0][0])
            row.append(data[key][0][1])
            values = []
            for item in data[key]:
                values.append(list(map(float, item[-1])))
            row += list(np.mean(values, axis=0))
            writer.writerow(row)

    print("%s rows added to file %s" %(len(data.keys()), fcc_out))
    # print("FCC Complete starting ACS file")

    # with open(acs_file) as csvread:
    #     reader = csv.reader(csvread)
    #     with open(acs_out, "w") as outfile:
    #         writer = csv.writer(outfile)
    #         count = 0
    #         for row in reader:
    #             count += 1
    #             if count % 100000==0:
    #                 print("%s rows completed" % count)
    #             out_row = [row[0].split("US")[-1]] + row[66:68] + row[2:6] + row[218:230] + row[602:610] + row[262:270]
    #             writer.writerow(out_row)
    # print("%s rows added to file %s" % (count, acs_out))

    # with open(fcc_out) as csvread:
    #     reader = csv.reader(csvread)
    #     header = True
    #     with open("data/fcc_merged.csv", "w") as csvout:
    #         writer = csv.writer(csvout)
    #         merge = [[]]
    #         count = 0
    #         for row in reader:
    #             if header:
    #                 header = False
    #                 writer.writerow(row)
    #                 continue
    #             if row[0] == merge[0]:
    #                 merge[2].append(row[2])
    #                 for i in range(3, 8):
    #                     merge[i].append(float(row[i]))
    #             else:
    #                 if not merge[0]:
    #                     merge = row[:2] + [[row[2]]] + [[float(k)] for k in row[3:]]
    #                     print(merge)
    #                 count += 1
    #                 out_row = [merge[0], merge[1], merge[2][0]+":"+merge[2][-1],
    #                            np.mean(merge[3]), np.mean(merge[4]), np.mean(merge[5]), np.mean(merge[6]), np.mean(merge[7])]
    #                 writer.writerow(out_row)
    #                 merge = row[:2] + [[row[2]]] + [[float(k)] for k in row[3:]]
    #     print("%s rows in fcc merge" %count)
    #

