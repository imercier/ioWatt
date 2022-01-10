#!/bin/bash -xe

pg_dump --format=tar \
  --dbname=postgresql://$PG_USER:$PG_PASS@$PG_HOST:$PG_PORT/$PG_DB \
  --file=pg_dump_$(date +%F).sql.tar
