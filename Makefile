NAME	:= ft_transcendence

DJANGODIR	:= ./backend/
DJANGO_SETTING	:= $(DJANGODIR)/ft_trans/settings.py

SRCDIR	:= ./frontend/
STATIC_DIR	:= $(SRCDIR)/public/

NGINX_IMAGE		:= docker-nginx
DB_IMAGE		:= docker-db
DJANGO_IMAGE	:= docker-django

DB_NET			:= db_net
DJANGO_NET		:= django_net

ENV_FILE	:= .env


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
	sudo rm -rf $(DJANGODIR)/.my_pgpass

re:
	@make fclean
	@make $(NAME)

init:
	-mkdir -p $(STATIC_DIR)/media
	-mkdir -p $(STATIC_DIR)/static

up:
	ln -f $(DJANGO_SETTING)_dev $(DJANGO_SETTING)
	python3 $(DJANGODIR)/manage.py runserver

update:
	docker-compose -f docker-compose.yml up -d --build

$(NAME):
	-mkdir -p $(STATIC_DIR)/media
	-mkdir -p $(STATIC_DIR)/static
	ln -f  $(DJANGO_SETTING)_pro $(DJANGO_SETTING)
	docker-compose   --env-file $(ENV_FILE)  -f docker-compose.yml up -d

stop:
	docker-compose -f docker-compose.yml down

.PHONY: all clean fclean re stop dev
