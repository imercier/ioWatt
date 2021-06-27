from psycopg2 import connect, extras
from os import environ
import json

pgHost = environ['PG_HOST']
pgDatabase = environ['PG_DB']
pgUser = environ['PG_USER']
pgPassword = environ['PG_PASS']

with open('formarted-data.json') as f:
    data = json.load(f)
    # transform list of list to list of tuple
    radiation = [tuple(x) for x in data['srad']]
    pression = [tuple(x) for x in data['slp']]
    temperature = [tuple(x) for x in data['temperature']]

    conn = None
    sqlRadiation = """INSERT INTO radiation
    (timestamp, radiation) VALUES %s
    ON CONFLICT("timestamp") DO NOTHING;"""

    sqlPression = """INSERT INTO pression
    (timestamp, pression) VALUES %s
    ON CONFLICT("timestamp") DO NOTHING;"""

    sqlTemperature = """INSERT INTO temperature
    (timestamp, temperature) VALUES %s
    ON CONFLICT("timestamp") DO NOTHING;"""

    try:
        conn = connect(
            host=pgHost,
            database=pgDatabase,
            user=pgUser,
            password=pgPassword)
        cur = conn.cursor()
        extras.execute_values(cur,
                              sqlRadiation,
                              radiation,
                              template='(to_timestamp(%s / 1000), %s)')
        extras.execute_values(cur,
                              sqlPression,
                              pression,
                              template='(to_timestamp(%s / 1000), %s)')
        extras.execute_values(cur,
                              sqlTemperature,
                              temperature,
                              template='(to_timestamp(%s / 1000), %s)')
    except (Exception) as error:
        print(error)
        if conn is not None:
            conn.rollback()
    else:
        conn.commit()
    finally:
        if conn is not None:
            conn.close()
