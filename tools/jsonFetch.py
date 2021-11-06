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
inverter_serial = environ['SOLAREDGE_INVERTER_SERIAL']


def dataFetch(startTime, endTime):
    req = endpoint + \
        '/equipment/' + \
        siteId + '/' + \
        inverter_serial + \
        '/data?' + \
        'startTime=' + quote(startTime) + \
        '&endTime=' + quote(endTime) + \
        '&api_key=' + api_key
    resp = get(req)
    if resp.status_code == 200:
        data = resp.json()['data']['telemetries']
        logging.debug(data)
        return data
    logging.error(resp)


def dataDbSave(cur, data):
    if data is not None:
        sql = """INSERT INTO jsonSeries
        (siteId, dateTime, apiVersion, data) VALUES (%s, %s, %s, %s)
        ON CONFLICT(siteId, dateTime)
        DO UPDATE SET data = %s;"""
        logging.info("Inserting %d measures", len(data))
        try:
            for d in data:
                logging.debug("Inserting: \"%s\"", dumps(d))
                cur.execute(sql, (siteId, d['date'], "1", dumps(d), dumps(d)))
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
        start = now - timedelta(weeks=1)
        startTime = start.strftime("%Y-%m-%d %H:%M:%S")
        end = now - timedelta(weeks=0)
        endTime = end.strftime("%Y-%m-%d %H:%M:%S")
        logging.info("Req: startTime: %s endTime: %s" % (startTime, endTime))
        dataDbSave(cur, dataFetch(startTime, endTime))
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
