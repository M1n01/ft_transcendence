FROM redis:bullseye
MAINTAINER hsano hsano@student.42tokyo.jp

RUN mkdir /etc/tls
RUN mkdir /etc/tls/ca
RUN apt-get update && apt-get upgrade -y && apt-get install vim openssl -y
COPY ./make_ca.sh /tmp/make_ca.sh
RUN chmod 744 /tmp/make_ca.sh
RUN sh /tmp/make_ca.sh
COPY tools/redis.conf0 /etc/redis/redis.conf0

CMD ["redis-server"]
