NAME	:= ft_transcendence

COMPOSEFILE	:= docker-compose.yml

DJANGODIR			:= ./django/
FRONTEND_DIR		:= $(DJANGODIR)/frontend/
DJANGO_STATIC_DIR	:= $(DJANGODIR)/public/
BACKEND_DIR			:=$(DJANGODIR)/backend/
SRCDIR				:= $(BACKEND_DIR)/ft_trans/
DJANGO_SETTING		:= $(SRCDIR)/settings.py
DJANGO_DEV_SETTING	:= $(SRCDIR)/settings_dev.py
DJANGO_PROD_SETTING	:= $(SRCDIR)/settings_prod.py

NGINX_IMAGE		:= ft_transcendence-nginx
DB_IMAGE			:= ft_transcendence-db
DJANGO_IMAGE	:= ft_transcendence-django
ETH_IMAGE	:= ft_transcendence-eth

DB_NET				:= db_net
DJANGO_NET		:= django_net
DB_VOLUME			:= ./db_volume

ENV_FILE			:= .env


all: $(NAME)

clean: stop
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	find . -type d -name __pycache__ -exec rm -r {} \+
	docker image rm $(DB_IMAGE) $(NGINX_IMAGE) $(DJANGO_IMAGE) $(ETH_IMAGE)

fclean:
	-$(MAKE) clean
	docker system prune -f
	docker volume prune -f
	docker network prune -f
	-rm django/backend/db.sqlite3
	-rm -rf $(DB_VOLUME) $(DJANGODIR)/.my_pgpass

re: fclean all

stop:
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) down

update: stop
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d --build

up:
	ln -f $(DJANGO_DEV_SETTING) $(DJANGO_SETTING)
	python $(BACKEND_DIR)/manage.py makemigrations
	python $(BACKEND_DIR)/manage.py migrate
	cd $(FRONTEND_DIR) && (npm start &) && python ../backend/manage.py runserver

dev:
	ln -f $(DJANGO_DEV_SETTING) $(DJANGO_SETTING)
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d
	docker exec -it django bash -c '(cd frontend && npm start &) && python ./backend/manage.py runserver 0.0.0.0:8001'

$(NAME):
	-mkdir -p $(addprefix $(DJANGO_STATIC_DIR), media static)
	ln -f $(DJANGO_PROD_SETTING) $(DJANGO_SETTING)
	docker-compose --env-file $(ENV_FILE) -f $(COMPOSEFILE) up -d


.PHONY: all clean fclean re stop up update dev
