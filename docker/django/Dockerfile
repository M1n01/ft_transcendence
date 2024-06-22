FROM python:3.11.9-slim-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install gettext procps postgresql-client iputils-ping net-tools  -y

WORKDIR /workspace

COPY ./.my_pgpass /tmp/.my_pgpass
COPY ./make_ca.sh /tmp/make_ca.sh
RUN python -m pip install --upgrade pip
RUN python -m pip install django-cors-headers
RUN python -m pip install Django==5.0.6
RUN python -m pip install daphne
RUN python -m pip install psycopg

RUN chmod 744 /tmp/make_ca.sh
RUN sh /tmp/make_ca.sh

#RUN python manage.py collectstatic

#COPY ./entrypoint.sh /workspace/entrypoint.sh
#ENTRYPOINT ["/workspace/entrypoint.sh"]
