#!/bin/bash
curl -s https://monitoringapi.solaredge.com/equipment/$SOLAREDGE_SITE_ID/list?api_key=$SOLAREDGE_API_KEY |jq
