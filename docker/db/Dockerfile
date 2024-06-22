FROM postgres:15.7-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install vim -y

COPY ./sql_data /tmp/
COPY ./exe_sql.sh /tmp/
RUN chmod 777 /tmp/exe_sql.sh
RUN chmod 777 /tmp
RUN eval "echo \"$(cat /tmp/sql_data)\"" > /tmp/tmp_sql

#RUN createuser -U postgres doc_test_user
#RUN createdb -U doc_test_user doc_test_db
#RUN sh /tmp/exe_sql.sh



