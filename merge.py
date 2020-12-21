import pandas as pd

fcc_file = "data/fcc2.csv"
acs_file = "data/acs2.csv"
outfile = "data/fcc_acc_merged.csv"

fcc = pd.read_csv(fcc_file)
acs = pd.read_csv(acs_file)
col = list(fcc.columns)
col[0] = 'id'
fcc.columns = col

out = fcc.join(acs.set_index('id'), on='id', how="left")
out.to_csv(outfile)



