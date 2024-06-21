FROM nginx:1.24.0-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
#RUN apt install -y ufw
RUN apt install -y vim
COPY ./django.conf /etc/nginx/conf.d/
COPY ./make_ca.sh /tmp/make_ca.sh
RUN rm /etc/nginx/conf.d/default.conf
RUN mv /etc/nginx/conf.d/django.conf /etc/nginx/conf.d/default.conf
#RUN update-alternatives --set iptables /usr/sbin/iptables-legacy
RUN chmod 744 /tmp/make_ca.sh
RUN chmod 755 /etc/nginx
RUN sh /tmp/make_ca.sh

#RUN ufw allow 443/tcp
#RUN ufw allow 80/tcp
#RUN ufw reload


WORKDIR /public

