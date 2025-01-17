import os
import pandas as pd
import numpy as np

temperatureFrame = pd.read_csv("temperature_dump_bkk.csv", index_col=0, usecols=[1, 2, 3, 4])
dustFrameProto = pd.read_csv("pm25_bkk.csv", index_col=0)
# consolidate data and put into data_vectors.csv

def season(dayFraction: float):
    if dayFraction > 0.8 or dayFraction < 0.25:
        return 1
    return 0

stationDict = {
    "02T": [13.7325,	100.4897],
    "03T": [13.6327,	100.4203],
    "05T": [13.6811,	100.5919],
    "10T": [13.7680,	100.6497],
    "11T": [13.7755,	100.5688],
    "12T": [13.7064,	100.5469],
    "50T": [13.7322,	100.5358],
    "52T": [13.7275,	100.4863],
    "53T": [13.7952,	100.5933],
    "54T": [13.7647,	100.5536],
    "59T": [13.7805,	100.5381],
    "61T": [13.7678,	100.6147]
}

mergedData = []
for row in dustFrameProto.itertuples():
    a = list(row)
    b, a = a[0], a[1:]
    if b in temperatureFrame.index:
        for i in range(len(a)):
            if pd.notna(a[i]):
                station = dustFrameProto.columns[i]
                mergedData.append([temperatureFrame.at[b, "year"], temperatureFrame.at[b, "day"], season(temperatureFrame.at[b, "day"]), temperatureFrame.at[b, "temp"], stationDict[station][0], stationDict[station][1], a[i]])

df = pd.DataFrame(mergedData, columns=["year", "dayFraction", "season", "temp", "lat", "long", "pm2.5"])
print(df)
df.to_csv(f"merged_data.csv")