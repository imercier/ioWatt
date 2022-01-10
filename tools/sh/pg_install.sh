#! /bin/bash
sudo apt-get install -qy postgresql
sudo -u postgres psql -d postgres -c "ALTER USER postgres PASSWORD 'camarche'"
#sudo passwd postgres

PG_HOST=iowatt.cailfs2k65yh.eu-west-3.rds.amazonaws.com
PG_DB=postgres
PG_USER=postgres
PG_PASS=QHL5UmFLGr
PG_PORT=5432

echo $PG_HOST:$PG_PORT:$PG_DB:$PG_USER:$PG_PASS >> $HOME/.pgpass
chmod 400 $HOME/.pgpass
