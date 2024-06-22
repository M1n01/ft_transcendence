FROM postgres:15.7-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install vim -y

COPY ./sql_data /docker-entrypoint-initdb.d/
COPY ./exe_sql.sh /docker-entrypoint-initdb.d/
#RUN chmod 777 /tmp
#RUN eval "echo \"$(cat /tmp/sql_data)\"" > /tmp/tmp_sql
#RUN chmod 777 /docker-entrypoint-initdb.d
#RUN chown postgres:postgres -R /docker-entrypoint-initdb.d/*


#RUN createuser -U postgres doc_test_user
#RUN createdb -U doc_test_user doc_test_db
#RUN sh /tmp/exe_sql.sh

