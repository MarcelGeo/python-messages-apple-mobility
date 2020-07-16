import numpy as np

def getData():
  path = "data/applemobilitytrends-2020-05-05.csv"
  npcsv = np.genfromtxt(path, delimiter=',')
  print(npcsv)

def getDataV2():
  path = "data/applemobilitytrends-2020-05-05.csv"
  npcsv = np.genfromtxt(path, delimiter=',', encoding='utf8')
  print(npcsv)

def getDataV4():
  path = "data/applemobilitytrends-2020-05-05.csv"
  npcsv = np.genfromtxt(path, delimiter=',', encoding='utf8', dtype=np.str, missing_values = np.nan, filling_values=np.nan)
  return npcsv

def convertData(data):
  converted = data[1:, 5:].astype(np.float)
  print(converted)

data = getDataV4()
convertData(data)