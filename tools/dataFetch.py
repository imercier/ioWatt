from requests import get
from datetime import datetime, timedelta
from pytz import timezone
from urllib.parse import quote
from psycopg2 import connect
from os import environ
import logging
from json import dumps

logger = logging.getLogger()
logger.setLevel(logging.INFO)

endpoint = 'https://monitoringapi.solaredge.com'
api_key = environ['SOLAREDGE_API_KEY']
siteId = environ['SOLAREDGE_SITE_ID']
pgHost = environ['PG_HOST']
pgDatabase = environ['PG_DB']
pgUser = environ['PG_USER']
pgPassword = environ['PG_PASS']


def powerFetch(startTime, endTime):
    req = endpoint + \
        '/site/' + siteId + \
        '/power?' + \
        '&startTime=' + quote(startTime) + \
        '&endTime=' + quote(endTime) + \
        '&api_key=' + api_key
    resp = get(req)
    if resp.status_code == 200:
        logging.debug(dumps(resp.json()))
        return resp.json()['power']['values']
    logging.error(resp)


def energyFetch(startTime, endTime):
    req = endpoint + \
        '/site/' + siteId + \
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


def dataDbSave(cur, data, sensor):
    if data is not None:
        sql = """INSERT INTO timeseries
        (siteId, timestamp, sensor, value) VALUES (%s, %s, %s, %s)
        ON CONFLICT(siteId, sensor, timestamp)
        DO UPDATE SET value = %s;"""
        logging.info("Inserting %d measures", len(data))
        try:
            for v in data:
                if not v.get('value') or v['value'] is None:
                    v['value'] = 0
                cur.execute(sql, (siteId, v['date'], sensor, v['value'], v['value']))
        except (Exception) as error:
            logging.error(error)


def lambda_handler(event, context):
    try:
        conn = connect(
            host=pgHost,
            database=pgDatabase,
            user=pgUser,
            password=pgPassword)
        cur = conn.cursor()
        now = datetime.now(timezone('Europe/Paris'))
        start = now - timedelta(weeks=4)
        startTime = start.strftime("%Y-%m-%d %H:%M:%S")
        endTime = now.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Req: startTime: %s endTime: %s" % (startTime, endTime))
        dataDbSave(cur, energyFetch(startTime, endTime), "energy")
        dataDbSave(cur, powerFetch(startTime, endTime), "power")
    except (Exception) as error:
        logging.error(error)
        if conn is not None:
            conn.rollback()
    else:
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    lambda_handler(None, None)
