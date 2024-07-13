NAME	:= ft_transcendence

COMPOSEFILE	:= docker-compose.yml

DJANGODIR	:= ./ft_trans/
DJANGO_STATIC_DIR	:= $(DJANGODIR)/public/
SRCDIR	:= $(DJANGODIR)/ft_trans/
DJANGO_SETTING	:= $(SRCDIR)/settings.py

NGINX_IMAGE		:= docker-nginx
DB_IMAGE			:= docker-db
DJANGO_IMAGE	:= docker-django

DB_NET				:= db_net
DJANGO_NET		:= django_net
DB_VOLUME			:= ./db_volume

ENV_FILE			:= .env


all: $(NAME)

clean: stop
	docker image rm $(DB_IMAGE) $(NGINX_IMAGE) $(DJANGO_IMAGE)

fclean:
	-$(MAKE) clean
	docker system prune -f
	docker volume prune -f
	docker network prune -f
	sudo rm -rf $(DB_VOLUME)/* $(DJANGODIR)/.my_pgpass

re: fclean all

up:
	ln -f $(DJANGO_SETTING)_dev $(DJANGO_SETTING)
	python $(DJANGODIR)/manage.py makemigrations
	python $(DJANGODIR)/manage.py migrate
	python3 $(DJANGODIR)/manage.py runserver

update:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d --build

$(NAME):
	-mkdir -p $(DJANGO_STATIC_DIR)/{media,static}
	ln -f $(DJANGO_SETTING)_pro $(DJANGO_SETTING)
	npx webpack
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d

dev:
	ln -f $(DJANGO_SETTING)_dev $(DJANGO_SETTING)
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d
	docker exec -it django bash -c 'python manage.py runserver 0:8001'

stop:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) down

.PHONY: all clean fclean re stop up update dev
