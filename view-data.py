# %%
import numpy as np
import pandas as pd


# %%
data = pd.read_csv("resource/6lo.csv")
data.index += 1

data.head(10)

# %%
data.head(10)["other"]