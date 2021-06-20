from requests import get
from datetime import datetime, timedelta
from pytz import timezone
from urllib.parse import quote
from psycopg2 import connect
from sys import exit
from os import environ
import logging
from json import dumps

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

endpoint = 'https://monitoringapi.solaredge.com'
api_key = environ['SOLAREDGE_API_KEY']
site_id = environ['SOLAREDGE_SITE_ID']
pgHost = environ['PG_HOST']
pgDatabase = environ['PG_DB']
pgUser = environ['PG_USER']
pgPassword = environ['PG_PASS']


def dataFetch():
    now = datetime.now(timezone('Europe/Paris'))
    start = now - timedelta(minutes=5)
    startTime = start.strftime("%Y-%m-%d %H:%M:%S")
    endTime = now.strftime("%Y-%m-%d %H:%M:%S")
    logging.info("Api req: startTime: %s endTime: %s" % (startTime, endTime))
    req = endpoint + \
        '/site/' + site_id + \
        '/energyDetails?' + \
        'meters=PRODUCTION' + \
        '&timeUnit=QUARTER_OF_AN_HOUR' + \
        '&startTime=' + quote(startTime) + \
        '&endTime=' + quote(endTime) + \
        '&api_key=' + api_key
    resp = get(req)
    if resp.status_code == 200:
        logging.debug(dumps(resp.json()))
        return resp.json()['energyDetails']['meters'][0]['values']
    logging.error(resp)
    exit(-1)


def dataDbSave(data):
    conn = None
    sql = """INSERT INTO EnergyHistory
    (timestamp, energyProduced, isValid) VALUES(%s, %s, %s)
    ON CONFLICT("timestamp")
    DO UPDATE SET energyProduced = %s, isValid = %s;"""
    logging.info("Inserting %d measures", len(data))
    try:
        conn = connect(
            host=pgHost,
            database=pgDatabase,
            user=pgUser,
            password=pgPassword)
        cur = conn.cursor()
        for v in data:
            isValid = True
            if not v.get('value') or v['value'] is None:
                v['value'] = 0
                isValid = False
            cur.execute(sql,
                        (v['date'], v['value'], isValid, v['value'], isValid))
    except (Exception) as error:
        logging.error(error)
        if conn is not None:
            conn.rollback()
    else:
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


def lambda_handler(event, context):
    data = dataFetch()
    dataDbSave(data)


if __name__ == "__main__":
    lambda_handler(None, None)
