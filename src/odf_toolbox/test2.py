import pandas as pd

data = {'Date': ['2023-01-01', '2023-01-01', '2023-01-02', '2023-01-02'],
        'City': ['New York', 'London', 'New York', 'London'],
        'Temperature': [10, 8, 12, 9]}
df = pd.DataFrame(data)
print(df)

# Pivot the DataFrame
df_wide = df.pivot(index='Date', columns='City', values='Temperature')
print(df_wide)
