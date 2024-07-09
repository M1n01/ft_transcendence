FROM python:3.11.9-slim-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install gettext procps postgresql-client iputils-ping net-tools  -y

WORKDIR /workspace
COPY ./make_ca.sh /tmp/make_ca.sh
COPY ./make_db_setting.sh /tmp/make_db_setting.sh
RUN python -m pip install --upgrade pip && \
python -m pip install django-cors-headers \
Django==5.0.6 \
daphne \
psycopg \
django-oauth-toolkit \
djangorestframework  \
qrcode \
requests


RUN chmod 744 /tmp/make_ca.sh
RUN sh /tmp/make_ca.sh

