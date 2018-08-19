import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data/finaldataset.csv')
plt.scatter(df['humid'],df['load'])
plt.show()