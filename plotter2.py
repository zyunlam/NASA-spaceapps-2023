import pandas as pd
from matplotlib import pyplot
df = pd.read_csv("values.csv", delimiter = ',', parse_dates=[0], infer_datetime_format=True, na_values='0')
df.set_index('Time', inplace=True)
df["Value"] = df.rolling("14D").mean()
df.plot()

pyplot.show()
