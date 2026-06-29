import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd

df = pd.read_csv("/Users/829005/Desktop/Monty Hall.csv")

ax=plt.axes(projection='3d')
df.plot(ax=ax)

plt.show()