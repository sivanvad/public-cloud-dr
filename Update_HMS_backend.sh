# DO NOT RUN THIS SCRIPT WITHOUT KNOWING WHAT YOU ARE DOING
# THIS WILL CORRUPT THE HIVE METASTORE IF NOT DONE CORRECTLY


# Run as root
source activate_salt_env

UPDATE_SQL_FILE=hms_update.sql

PGPASSWORD=$(salt-call pillar.get postgres:hive:remote_admin_pw| tail -n 1 | awk '{print $1}')

HIVE_DB=$(salt-call pillar.get postgres:hive:database| tail -n 1 | awk '{print $1}')

HIVE_DB_REMOTE_ADM=$(salt-call pillar.get postgres:hive:remote_admin| tail -n 1 | awk '{print $1}')

HIVE_DB_REMOTE_PORT=$(salt-call pillar.get postgres:hive:remote_db_port| tail -n 1 | awk '{print $1}')

HIVE_DB_REMOTE_URL=$(salt-call pillar.get postgres:hive:remote_db_url| tail -n 1 | awk '{print $1}')


psql -h ${HIVE_DB_REMOTE_URL} -U ${HIVE_DB_REMOTE_ADM} -p ${HIVE_DB_REMOTE_PORT} -d ${HIVE_DB} -a -f ${UPDATE_SQL_FILE}