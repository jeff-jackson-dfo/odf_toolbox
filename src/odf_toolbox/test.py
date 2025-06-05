import pandas as pd
import numpy as np

# Create a Pandas Series
s1 = pd.Series([10, 20, 30, 40, 50], index=['A', 'B', 'C', 'D', 'E'])
s2 = pd.Series([2, 5, 0, 10, np.nan], index=['A', 'B', 'C', 'D', 'E'])

# Divide s1 by s2
result = s1.div(s2, fill_value=0)
result_cleaned = result.replace([np.inf, -np.inf], 0)
print(result_cleaned)
