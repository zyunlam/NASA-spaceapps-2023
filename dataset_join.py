import pandas as pd
import numpy as np
import json

DSCOVR_data = pd.read_csv("DSCOVR.csv", na_values='0')
DSCOVR_data.set_index('Time', inplace=True)

#magnetic_lat = radians(86.494)
#magnetic_long = radians(162.867)

data = []
for k in range(16, 24):
    data.append(pd.read_csv(f"data\dsc_fc_summed_spectra_20{k}_v01.csv", na_values="0", header=None))

magnetic_data = pd.concat(data)
magnetic_data.set_index(0, inplace=True)
magnetic_data = magnetic_data.iloc[:, : 3]
magnetic_data = magnetic_data.rename(columns={0: "Time", 1:"bx", 2:"by", 3:"bz"})
magnetic_data.index.name = "Time"
database = {}
print(magnetic_data)
print(magnetic_data.index.inferred_type)
print(DSCOVR_data.index.inferred_type)
print(DSCOVR_data)
for index, data in magnetic_data.iterrows():
    if index in DSCOVR_data.index:
        database[index] = {**(data.to_dict()), **(DSCOVR_data.loc[index].to_dict())}
print("Done")
with open("combined.json", "w") as f:
    f.write(json.dumps(database))
