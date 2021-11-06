import requests
from datetime import datetime, timedelta
from pytz import timezone
import urllib.parse
import logging
from os import environ
from sys import exit
import json

logging.basicConfig(level=logging.INFO)

endpoint = 'https://monitoringapi.solaredge.com'
api_key = environ['SOLAREDGE_API_KEY']
site_id = environ['SOLAREDGE_SITE_ID']

now = datetime.now(timezone('Europe/Paris'))
start = now - timedelta(days=1)
end = now - timedelta(days=0)
startTime = start.strftime("%Y-%m-%d %H:%M:%S")
startTime = start.strftime("2021-10-28 00:00:00")
endTime = end.strftime("%Y-%m-%d %H:%M:%S")
endTime = start.strftime("2021-10-30 00:00:00")


inverter_serial = environ['SOLAREDGE_INVERTER_SERIAL']
req = endpoint + \
    '/equipment/' + \
    site_id + '/' + \
    inverter_serial + \
    '/data?' + \
    'startTime=' + urllib.parse.quote(startTime) + \
    '&endTime=' + urllib.parse.quote(endTime) + \
    '&api_key=' + api_key
resp = requests.get(req)
if resp.status_code == 200:
    resp = requests.get(req).json()
    print(json.dumps(resp))
else:
    print(resp)
"""
req = endpoint + \
      '/site/' + site_id + \
      '/power?' + \
      'startTime=' + urllib.parse.quote(startTime) + \
      '&endTime=' + urllib.parse.quote(endTime) + \
      '&api_key=' + api_key
resp = requests.get(req)
if resp.status_code == 200:
    resp = requests.get(req).json()['power']['values']
    print(json.dumps(resp))
else:
    print(resp)
exit()

req = endpoint + \
      '/site/' + site_id + \
      '/inventory?' + \
      '&api_key=' + api_key
resp = requests.get(req)
if resp.status_code == 200:
    resp = requests.get(req).json()
    print(json.dumps(resp))
else:
    print(resp)
exit()
"""
