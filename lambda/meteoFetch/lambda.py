from psycopg2 import connect, extras
from requests import get
from os import environ
from json import loads
import logging
from re import finditer, MULTILINE
import sys

pgHost = environ['PG_HOST']
pgDatabase = environ['PG_DB']
pgUser = environ['PG_USER']
pgPassword = environ['PG_PASS']
infoClimatUrl = environ['METEO_URL']


def lambda_handler(event, context):
    response = get(infoClimatUrl)
    if response.status_code != 200:
        logging.error(response)
        return response.status_code
    regex = (r"var _data_gr = (.*).$\n")
    matches = finditer(regex, response.text, MULTILINE)
    for match in matches:
        data = loads(match.group(1))
        break
    # transform list of list to list of tuple
    #print(data['slp'][162])
    pression = [tuple(x) for x in data['slp'] if isinstance(x, list)]
    radiation = [tuple(x) for x in data['srad']  if isinstance(x, list)]
    temperature = [tuple(x) for x in data['temperature']  if isinstance(x, list)]

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


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    lambda_handler(None, None)
