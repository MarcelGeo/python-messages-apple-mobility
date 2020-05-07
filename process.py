import numpy as np
import store
import tasks
import psycopg2
import pre
import filters
import after

conn = pre.connect()

print(store.__STORE__)

store.initStore(data=np.array([]), dates=np.array([], dtype="datetime64"), today=None)
tasks.prepareDate()
tasks.getData()
tasks.getDates()
tasks.addDataToDB(conn, filters.getMaxDateFromDb(conn, store.mapStore("dates")))
tasks.addPercentileMessageToDB()
exceptions = store.mapStore("exceptions")
today = store.mapStore("today")
end = after.end(conn, today, len(exceptions) < 1)


conn.close()


