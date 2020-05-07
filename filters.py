import psycopg2
import numpy as np

def getMaxDateFromDb(conn, inputData):
  try:
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date) FROM apple_transport")
    maxDate = cursor.fetchone()[0]
    cursor.close()
    if(maxDate is not None):
      npdate = np.datetime64(maxDate)
      return inputData > npdate
    else:
      return None
  except psycopg2.DatabaseError as e:
    cursor.close()
    return False

def filterStates(inputData, transportation_type="walking"):
  filtering = inputData[:, 0]
  indexFiltering = filtering == 'country/region'
  filteringData = inputData[indexFiltering, :]
  transportationIndex = filteringData[:, 2] == transportation_type
  return filteringData[transportationIndex, :]

def filterPercentiles(inputData, percentile):
  value = np.percentile(inputData[:, -1].astype(np.float), percentile)
  return inputData[:, -1].astype(np.float) <= value, inputData[:, -1].astype(np.float) > value, value

def filerOver100(inputData):
  return inputData[:, -1].astype(np.float) >= 100





