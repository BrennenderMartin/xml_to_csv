import pandas as pd

df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],
                    index=['cobra', 'viper', 'sidewinder'],
                    columns=['max_speed', 'shield'])

#df.to_csv("Test8.csv", sep=";", index=False)

daten = pd.read_csv("Test8.csv", sep=";")
df = pd.DataFrame(daten)
df.at[0, "max_speed"] = 5
print(df)
#df.to_csv("Test8.csv", sep=";")