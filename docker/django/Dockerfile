FROM python:3.11.9-slim-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install gettext procps postgresql-client iputils-ping net-tools curl -y
ENV NVM_VERSION v0.39.7
ENV NVM_DIR /usr/local/nvm
#ENV NODE_VERSION v20.15.1
ENV NODE_VERSION v21.4.0
# ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

RUN mkdir /usr/local/nvm \
    && curl https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VERSION/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use  default \
    && ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/node /usr/bin/nodejs \
    && ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/node /usr/bin/node \
    && ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/npm /usr/bin/npm \
    && ln -sf $NVM_DIR/versions/node/$NODE_VERSION/bin/yarn /usr/bin/yarn

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
requests \
django-webpack-loader \
djangorestframework \
web3 \
py-solc-x \
pyjwt \
sendgrid \
twilio \
django-phonenumber-field[phonenumberslite] \
sib_api_v3_sdk \
pyotp
#django-twilio

RUN chmod 744 /tmp/make_ca.sh
RUN sh /tmp/make_ca.sh
