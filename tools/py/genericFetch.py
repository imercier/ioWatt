from requests import get
import time
from datetime import datetime, timedelta
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


def equipmentFetch(startTime, endTime):
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


def dataDbSave(cur, execTime, label, data):
    if data is not None:
        sql = """INSERT INTO ioWatt_utc
        (siteId, execTime, label, apiVersion, data) VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (siteId, label, datatime)
        DO UPDATE SET exectime = %s, data = %s;"""
        logging.info("Inserting %d measures for label: %s", len(data), label)
        try:
            for d in data:
                logging.debug("Inserting: \"%s\"", dumps(d))
                cur.execute(sql,
                            (siteId,
                             execTime,
                             label,
                             "unknow",
                             dumps(d),
                             execTime,
                             dumps(d)))
        except (Exception) as error:
            logging.error(error)


def process(start, end):
    startTime = start.strftime("%Y-%m-%d %H:%M:%S")
    endTime = end.strftime("%Y-%m-%d %H:%M:%S")
    logging.info("Req: startTime: %s endTime: %s" % (startTime, endTime))
    try:
        conn = connect(
            host=pgHost,
            database=pgDatabase,
            user=pgUser,
            password=pgPassword)
        cur = conn.cursor()
        dataDbSave(cur,
                   time.strftime('%Y-%m-%d %H:%M:%S'),
                   "power",
                   powerFetch(startTime, endTime))
        execTime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        dataDbSave(cur,
                   execTime,
                   "equipment_inverter",
                   equipmentFetch(startTime, endTime))
        execTime = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        dataDbSave(cur,
                   execTime,
                   "energy",
                   energyFetch(startTime, endTime))
    except (Exception) as error:
        logging.error(error)
    else:
        conn.commit()
        conn.close()


if __name__ == "__main__":
    start = datetime(2021, 11, 9)
    now = datetime.today()
    end = datetime(1900, 1, 1)
    while end != now:
        end = start + timedelta(weeks=1)
        if end > now:
            end = now
        process(start, end)
        start += timedelta(weeks=1)
