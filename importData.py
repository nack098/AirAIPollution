import os
import pandas as pd
import numpy as np

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getTemperatureProbeLocation(filepath: str):
    """
        Helper function to obtain current probe location reference.
        Input: filepath of temperature probe metadata
        Output: dict with key each probe station code and lat-long as value.
    """
    temperatureProbe = {}
    df = pd.read_csv(filepath)
    for row in df.itertuples(index=False):
        if(temperatureProbe.get(row.code) == None):
            temperatureProbe[row.code] = []
        temperatureProbe.get(row.code).append(np.array([row.lat, row.long]))
    for key in temperatureProbe:
        temperatureProbe[key] = np.average(np.array(temperatureProbe.get(key)),axis=0)
    return temperatureProbe

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

# preparation of temperature probe dictionary
stationMetadata = getTemperatureProbeLocation("0station_metadata.csv")
print("Loaded default location reference at: 0station_metadata.csv")
for root, dirs, files in os.walk("Temperature"):
    for file in files:
        file_path = os.path.join(root, file)
        if "metadata" in file_path:
            print("Update with new location reference:", file_path)
            tmp = getTemperatureProbeLocation(file_path)
            stationMetadata.update(tmp)
print("Load probe dictionary OK")
print("Dumping probe dictionary data")
df = pd.DataFrame(stationMetadata, ["lat", "long"])
print(df)
df.to_csv("Clean\\station_metadata.csv")

print("Loading temperature probe data")
temperatureData = {}
for station in stationMetadata:
    temperatureData[station] = []
temperatureDataDump = {}

file_count = 0
current_year = 2012
for root, dirs, files in os.walk("Temperature\\2012"):
    for file in files:
        file_path = os.path.join(root, file)
        if "metadata" not in file_path:
            file_count += 1
            if file_count == 100:
                file_count = 0
                print(file_path)
            tmp = file_path.split("\\")
            # obtain labels
            year = int(tmp[-3])
            month = int(tmp[-2][4:])
            code = tmp[-1][:-4]
            if code not in stationMetadata:
                continue

            # data is so large i have to dump it before it finishes
            if year != current_year:
                print(f"Reformatting temperature probe data for year {current_year}")
                df = pd.DataFrame(temperatureDataDump.get(current_year), columns=["code", "year", "month", "day", "temp"])
                print(df)
                df.to_csv(f"Clean\\temperature_dump_{current_year}.csv")
                del temperatureDataDump[current_year]
                current_year = year
                print(f"Continuing with probe data for year {year}")

            data = getTemperatureProbeData(file_path)
            # have year, month, and data with len equal to day (of a single probe)
            for day in range(len(data)):
                if pd.notna(data[day]):
                    temperatureData.get(code).append([year, month, day+1, data[day]])
                    if(temperatureDataDump.get(year) == None):
                        temperatureDataDump[year] = []
                    temperatureDataDump.get(year).append([code, year, month, day+1, data[day]])

print(f"Reformatting temperature probe data for year {current_year}")
df = pd.DataFrame(temperatureDataDump.get(current_year), columns=["code", "year", "month", "day", "temp"])
print(df)
df.to_csv(f"Clean\\temperature_dump_{current_year}.csv")
del temperatureDataDump[current_year]
current_year = year
print(f"Continuing with probe data for year {year}")