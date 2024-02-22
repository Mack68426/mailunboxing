# %%
import warnings

warnings.filterwarnings("ignore", "\nPyarrow", DeprecationWarning)
import numpy as np
import pandas as pd


# %%
data = pd.read_csv("6lo.csv")
data.index += 1

top_5 = data.head(5)

# %%
other_field = data.head(10)["other"]


# %%
print(data.shape[0])
# %%
