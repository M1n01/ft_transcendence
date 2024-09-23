FROM redis:bullseye
MAINTAINER hsano hsano@student.42tokyo.jp

RUN mkdir /etc/tls
RUN apt update && apt upgrade -y
RUN apt install -y vim openssl
COPY ./make_ca.sh /tmp/make_ca.sh
RUN chmod 744 /tmp/make_ca.sh
RUN sh /tmp/make_ca.sh
#COPY tools/redis.conf /etc/redis/redis.conf

#CMD ["redis-server", "/etc/redis/redis.conf"]
CMD ["redis-server"]
#CMD ["bash"]
#CMD ["/usr/sbin/php-fpm7.4", "-F"]
