FROM nginx:1.24.0-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
COPY ./django.conf /etc/nginx/conf.d/
RUN rm /etc/nginx/conf.d/default.conf
RUN mv /etc/nginx/conf.d/django.conf /etc/nginx/conf.d/default.conf
#COPY ./django.conf /etc/nginx/conf.d/default.conf


WORKDIR /public

