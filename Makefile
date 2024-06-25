NAME	:= ft_transcendence
YMLDIR	:= ./docker
DOCKERDIR	:= ./docker
DJANGODIR	:= ./ft_trans/
DJANGO_STATIC_DIR	:= $(DJANGODIR)/public/
SRCDIR	:= $(DJANGODIR)/ft_trans/
DJANGO_SETTING	:= $(SRCDIR)/settings.py

NGINX_IMAGE		:= docker-nginx
DB_IMAGE		:= docker-db
DJANGO_IMAGE	:= docker-django

DB_NET			:= db_net
DJANGO_NET		:= django_net

ENV_FILE	:= .env


DEPDIR			:= $(DBDIR)
DOCKERFILE		:= Dockerfile

VOLUME_DB			:= mariadb_volume
VOLUME_WP			:= wordpress_volume
NETWORK				:= inception_net


all:
	@make $(NAME)

clean:
	@make stop
	docker image rm $(DB_IMAGE)
	docker image rm $(NGINX_IMAGE)
	docker image rm $(DJANGO_IMAGE)

fclean:
	@make clean
	docker volume prune
	docker network prune
	sudo rm -rf db_volume/*
	sudo rm -rf ft_trans/.my_pgpass

re:
	@make fclean
	@make $(NAME)

init:
	-mkdir -p $(DJANGO_STATIC_DIR)/media
	-mkdir -p $(DJANGO_STATIC_DIR)/static

up:
	-rm $(DJANGO_SETTING)
	cp $(DJANGO_SETTING)_dev $(DJANGO_SETTING)
	sed -i "s/DEBUG\s*=\s*False/DEBUG = True/" $(DJANGO_SETTING)
	sed -i "s/django.core.cache.backends.locmem.LocMemCache/django.core.cache.backends.dummy.DummyCache/" $(DJANGO_SETTING)
	python ft_trans/manage.py runserver


update:
	docker-compose -f docker/docker-compose.yml up -d --build

$(NAME):
	-mkdir -p $(DJANGO_STATIC_DIR)/media
	-mkdir -p $(DJANGO_STATIC_DIR)/static
	-rm $(DJANGO_SETTING)
	cp $(DJANGO_SETTING)_pro $(DJANGO_SETTING)
	sed -i	"s/DEBUG\s*=\s*True/DEBUG = False/" $(DJANGO_SETTING)
	sed -i	"s/django.core.cache.backends.dummy.DummyCache/django.core.cache.backends.locmem.LocMemCache/" $(DJANGO_SETTING)
	docker-compose   --env-file $(ENV_FILE)  -f docker/docker-compose.yml up -d

stop:
	docker-compose -f docker/docker-compose.yml down

.PHONY: all clean fclean re stop dev 
