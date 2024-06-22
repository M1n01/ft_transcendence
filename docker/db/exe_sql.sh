#eval "echo \"$(cat /tmp/sql_data)\"" > /tmp/tmp_sql

#pg_ctl -D ${PGDATA} start -U postgres
#groupadd -r ${POSTGRES_DJANGO_USER} && useradd -r -g ${POSTGRES_DJANGO_USER} ${POSTGRES_DJANGO_USER} --home-dir /tmp/docker
createuser -U postgres ${POSTGRES_DJANGO_USER} --password  ${POSTGRES_DJANGO_PASSWORD}
createdb -U ${POSTGRES_DJANGO_USER} ${POSTGRES_DJANGO_DB_NAME}


