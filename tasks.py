import numpy as np
from datetime import date, timedelta, datetime
from pytz import timezone
import store
import psycopg2
import requests
import os
import filters

FIRST = 4

def prepareDate():
  pc_tz = timezone('US/Pacific')
  n = datetime.now(pc_tz)
  nd = n.date()
  store.updateStore(today=nd)

def getData():
  today = store.mapStore("today")
  npdata = store.mapStore("data")
  filedate = np.datetime64(today - timedelta(days=2))
  try:
    url = 'https://covid19-static.cdn-apple.com/covid19-mobility-data/2007HotfixDev49/v2/en-us/applemobilitytrends-{}.csv'.format(filedate)
    download = requests.get(url)
    download.encoding = "utf-8"
    temp_file = open("temp/temp.csv", 'w', encoding='utf8')
    temp_file.writelines(download.text)
    npcsv = np.genfromtxt("temp/temp.csv", delimiter=',', dtype=np.str, encoding='utf8', invalid_raise=False, missing_values = np.nan, filling_values=np.nan)
    temp_file.close()
    store.updateStore(data=npcsv)
    print(npcsv)
  except Exception as e:
    exceptions = store.mapStore("exceptions")
    exceptions.append(e)
    print("Not possible to read csv file .")
    print(e)

def getDates():
  dates = store.mapStore("dates")
  data = store.mapStore("data")
  exceptions = store.mapStore("exceptions")
  if(len(exceptions) > 0):
    return False
  try:
    d0 = date(2020, 1, 13)
    d1 = data[0,FIRST:]
    i = 0
    newdates = []
    while i <= d1.shape[0] - 1:
      diffday = np.datetime64(d0 + timedelta(days=i))
      newdates.append(diffday)
      i += 1
    newdates = np.concatenate((dates, newdates))
    store.updateStore(dates=newdates)
  except Exception as e:
    exceptions = store.mapStore("exceptions")
    exceptions.append(e)
    print("Problems with handling data numpy array")
    print(e)
  return True

def addDataToDB(conn, filterData):
  data = store.mapStore("data")
  dates = store.mapStore("dates")
  exceptions = store.mapStore("exceptions")
  if(len(exceptions) > 0):
    return False
  dataValues = data[1:,FIRST:]
  datesValues = dates
  if(filterData is not None):
    datesValues = datesValues[filterData]
    dataValues = dataValues[:,filterData]
  sql = "INSERT INTO apple_transport(geo_type, region, transportation_type, alternative_name, date, value) VALUES(%s, %s, %s, %s, %s, %s)"
  for ix,iy in np.ndindex(dataValues.shape):
    try:
      date = datesValues[iy].astype(datetime)
      values = data[ix+1, :FIRST]
      values = tuple(values.tolist())
      item = dataValues[ix, iy].item()
      try:
         item = float(item)
      except:
         item = None
      values = values + tuple([date, item])
      cursor = conn.cursor()
      cursor.execute(sql, values)
      conn.commit()
      cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
      exceptions = store.mapStore("exceptions")
      exceptions.append(error)

def addPercentileMessageToDB():
  data = store.mapStore("data")
  states_walking = filters.filterStates(data[1:, :])
  states_driving = filters.filterStates(data[1:, :], "driving")
  states_transit = filters.filterStates(data[1:, :], "transit")
  underq1, overq1, percentile_walking_25 = filters.filterPercentiles(states_walking, 25)
  undermedian, overmedian, percentile_walking_50 = filters.filterPercentiles(states_walking, 50)
  underq3, overq3, percentile_walking_75 = filters.filterPercentiles(states_walking, 75)

  underq1_driving, overq1_driving, percentile_driving_25 = filters.filterPercentiles(states_driving, 25)
  undermedian_driving, overmedian_driving, percentile_driving_50 = filters.filterPercentiles(states_driving, 50)
  underq3_driving, overq3_driving, percentile_driving_75 = filters.filterPercentiles(states_driving, 75)

  underq1_transit, overq1_transit, percentile_transit_25 = filters.filterPercentiles(states_transit, 25)
  undermedian_transit, overmedian_transit, percentile_transit_50 = filters.filterPercentiles(states_transit, 50)
  underq3_transit, overq3_transit, percentile_transit_75 = filters.filterPercentiles(states_transit, 75)

  over100_waling = filters.filerOver100(states_walking)
  underq1_states = states_walking[underq1,1]
  overq3_states = states_walking[overq3,1]
  over100_states = states_walking[over100_waling, 1]

  over100_driving = filters.filerOver100(states_driving)
  underq1_states_driving = states_driving[underq1_driving,1]
  overq3_states_driving = states_driving[overq3_driving,1]
  over100_states_driving = states_driving[over100_driving, 1]

  over100_transit = filters.filerOver100(states_transit)
  underq1_states_transit = states_transit[underq1_transit,1]
  overq3_states_transit = states_transit[overq3_transit,1]
  over100_states_transit = states_transit[over100_transit, 1]
  print("walking under 25 percentile (far to normal) " + percentile_walking_25.astype(np.str))
  print(underq1_states)
  print("walking over 75 percentile (over normal trnasportation) " + percentile_walking_75.astype(np.str))
  print(overq3_states)
  print("walking over 100 in comparison to 13.1.2020")
  print(over100_states)
  print("Median value is " + percentile_walking_50.astype(np.str))
  print("  ")

  print("Driving under 25 percentile (far to normal) " + percentile_driving_25.astype(np.str))
  print(underq1_states_driving)
  print("Driving over 75 percentile (over normal trnasportation) ", percentile_driving_75.astype(np.str))
  print(overq3_states_driving)
  print("Driving over 100% in comparison to 13.1.2020")
  print(over100_states_driving)
  print("Median value is " + percentile_driving_50.astype(np.str))
  print("  ")

  print("Transit under 25 percentile (far to normal) " + percentile_transit_25.astype(np.str))
  print(underq1_states_transit)
  print("Transit over 75 percentile (over normal trnasportation) ", percentile_transit_75.astype(np.str))
  print(overq3_states_transit.astype(np.str))
  print("Transit over 100 in comparison to 13.1.2020")
  print(over100_states_transit)
  print("Median value is " + percentile_transit_50.astype(np.str))
  print("  ")


    

  
  
