FROM nginx:1.25.0-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt-get update && apt-get upgrade -y && apt-get install vim -y
COPY ./django.conf /etc/nginx/conf.d/
COPY ./make_ca.sh /tmp/make_ca.sh
RUN rm /etc/nginx/conf.d/default.conf
RUN mv /etc/nginx/conf.d/django.conf /etc/nginx/conf.d/default.conf
RUN chmod 744 /tmp/make_ca.sh
RUN chmod 755 /etc/nginx
RUN sh /tmp/make_ca.sh

WORKDIR /public

