# Read DSCOVR2.csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('DSCOVR.csv', delimiter = ',', parse_dates=[0], infer_datetime_format=True, na_values='0')
df.set_index('Time', inplace=True)
# Plot a 3d graph on the position of the satellite
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot3D(df['X'], df['Y'], df['Z'], 'gray')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Show plot
plt.show()
