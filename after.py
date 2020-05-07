import psycopg2

def end(conn, today, success):
  try:
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM analysis_history")
    maxId = cursor.fetchone()[0]
    if(maxId is not None):
      maxId = maxId + 1
    else:
      maxId = 0
    cursor.execute("INSERT INTO analysis_history(id, date, success) VALUES (%s, %s, %s)", (maxId, today, success))
    cursor.close()
  except psycopg2.DatabaseError as e:
    cursor.close()
    return False