import os
import pandas as pd
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def dayFraction(day: int, month: int, year: int):
    total = 365.0
    norm = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    for i in range(month-1):
        day += norm[i]
    if(year % 4 == 0):
        day += 1
        total += 1
    if(year % 100 == 0):
        day -= 1
        total -= 1
    if(year % 400 == 0):
        day += 1
        total += 1
    return day/total
    
def getTemperatureProbeData(filepath: str):
    """
        Helper function to obtain daily temperature data from probe
        Input: filepath of temperature probe data
        Output: ndarray of temperatures equal to number of days
    """
    # parse file
    temperatureData = []
    tmp = []
    i = 0
    df = pd.read_csv(filepath)
    for row in df.itertuples(index=False):
        
        # validate data (ensure is number and is not lower than -100)
        if is_number(row[2]):
            check = float(row[2])
            if(check > -100):
                tmp.append(float(check))

        # splice every 24 entries
        i += 1
        if i == 24:
            i = 0
            if(len(tmp) == 0):
                temperatureData.append(np.nan)
            else:
                temperatureData.append(np.average(tmp))
            tmp.clear()
    
    return temperatureData
    
stationMetadata = {
    "CPY015": [13.700287, 100.492805]
}
temperatureDataDump = []

file_count = 0
current_year = 2012
for root, dirs, files in os.walk("Temperature"):
    for file in files:
        file_path = os.path.join(root, file)
        if "CPY015" in file_path:
            print(file_path)
            tmp = file_path.split("\\")
            # obtain labels
            year = int(tmp[-3])
            month = int(tmp[-2][4:])
            code = tmp[-1][:-4]

            data = getTemperatureProbeData(file_path)
            # have year, month, and data with len equal to day (of a single probe)
            for day in range(len(data)):
                if pd.notna(data[day]):
                    temperatureDataDump.append([str(day+1)+"/"+str(month)+"/"+str(year), year, dayFraction(day, month, year), data[day]])

print(f"Reformatting temperature probe data for bangkok")
df = pd.DataFrame(temperatureDataDump, columns=["date", "year", "day", "temp"])
print(df)
df.to_csv(f"temperature_dump_bkk.csv")
