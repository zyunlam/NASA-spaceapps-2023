import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# open csv file
df = pd.read_csv('dsc_fc_summed_spectra_2017_v01.csv', delimiter = ',', parse_dates=[0], infer_datetime_format=True, na_values='0', header = None)
# For columns 1-3, get the magnitue of the vector
df[1] = np.sqrt(df[1]**2 + df[2]**2 + df[3]**2)
# Get 3 day moving average of the magnitude
df[1] = df[1].rolling(3000).mean()

# Plot columns 0 and 1

#plt.plot(df[0], df[1])

# Read all the dates
frames = []
for i in range(1, 31):
    frames.append(pd.read_csv(f"xtaajuusraporttitaajuusdata2017csv-tiedostot-nettiin2017-11/2017-11-{i:02d}.csv", delimiter = ',', parse_dates=[0], infer_datetime_format=True, na_values='0'))
df2 = pd.concat(frames)
df2.set_index('Time', inplace=True)
print(df2)
df2["1HMA"] = df2['Value'].rolling("1H").mean()
df2["STD"] = df2['Value'].rolling("1H").std()
# Get the distance from standard deviation
df2["Distance"] = (df2['Value'] - df2["1HMA"]) / df2["STD"]
# "Value", "1HMA", 
df2.plot(y=["Distance", "STD"])
#plt.plot(df2['Time'], df2['Value'])
#plt.plot(df2['Time'], df2['1HMA'])

plt.show()
