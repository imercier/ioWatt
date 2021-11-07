from astral import LocationInfo
from astral.sun import sun
from datetime import date, timedelta
from pytz import timezone
from psycopg2 import connect
from os import environ

pgHost = environ['PG_HOST']
pgDatabase = environ['PG_DB']
pgUser = environ['PG_USER']
pgPassword = environ['PG_PASS']

city = LocationInfo("Marseille", "France", "Europe/Paris", 43.3, 5.4)
print((
    f"Information for {city.name}/{city.region}\n"
    f"Timezone: {city.timezone}\n"
    f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
))

tz = timezone('Europe/Paris')
start_date = date(2021, 1, 1)
end_date = date(2021, 12, 31)
delta = timedelta(days=1)
sunList = []
while start_date <= end_date:
    s = sun(city.observer, date=start_date, tzinfo=tz)
    element = [start_date, s["sunrise"], s["sunset"], city.name]
    sunList.append(element)
    start_date += delta

conn = None
sql = """INSERT INTO sunEphemeride
(day, sunrise, sunset, locationName) VALUES(%s, %s, %s, %s);"""
try:
    conn = connect(
        host=pgHost,
        database=pgDatabase,
        user=pgUser,
        password=pgPassword)
    cur = conn.cursor()
    cur.executemany(sql, sunList)
except (Exception) as error:
    print(error)
    if conn is not None:
        conn.rollback()
else:
    conn.commit()
finally:
    if conn is not None:
        conn.close()
