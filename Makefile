NAME	:= ft_transcendence

COMPOSEFILE	:= docker-compose.yml

DJANGODIR	:= ./ft_trans/
DJANGO_STATIC_DIR	:= $(DJANGODIR)/public/
SRCDIR	:= $(DJANGODIR)/ft_trans/
DJANGO_SETTING	:= $(SRCDIR)/settings.py
DJANGO_DEV_SETTING	:= $(SRCDIR)/settings_dev.py
DJANGO_PROD_SETTING	:= $(SRCDIR)/settings_prod.py

NGINX_IMAGE		:= docker-nginx
DB_IMAGE			:= docker-db
DJANGO_IMAGE	:= docker-django

DB_NET				:= db_net
DJANGO_NET		:= django_net
DB_VOLUME			:= ./db_volume

ENV_FILE			:= .env


all: $(NAME)

clean: stop
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	docker image rm $(DB_IMAGE) $(NGINX_IMAGE) $(DJANGO_IMAGE)

fclean:
	-$(MAKE) clean
	docker system prune -f
	docker volume prune -f
	docker network prune -f
	-rm -rf $(DB_VOLUME)/* $(DJANGODIR)/.my_pgpass

re: fclean all

up:
	ln -f $(DJANGO_DEV_SETTING) $(DJANGO_SETTING)
	python $(DJANGODIR)/manage.py makemigrations
	python $(DJANGODIR)/manage.py migrate
	python3 $(DJANGODIR)/manage.py runserver

update:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d --build

dev:
	ln -f $(DJANGO_DEV_SETTING) $(DJANGO_SETTING)
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d
	echo "docker exec -it django bash -c 'npm start &&   python manage.py runserver 0:8001'"

stop:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) down

$(NAME):
	-mkdir -p $(DJANGO_STATIC_DIR)/{media,static}
	ln -f $(DJANGO_PROD_SETTING) $(DJANGO_SETTING)
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d

.PHONY: all clean fclean re stop up update dev
