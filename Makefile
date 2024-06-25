NAME	:= ft_transcendence
YMLDIR	:= ./docker
DOCKERDIR	:= ./docker
DJANGODIR	:= ./ft_trans/
DJANGO_STATIC_DIR	:= $(DJANGODIR)/public/
SRCDIR	:= $(DJANGODIR)/ft_trans/
DJANGO_SETTING	:= $(SRCDIR)/settings.py

NGINX	:= nginx
DB		:= db

NGINXDIR		:= $(addprefix $(DOCKERDIR)/, $(NGINX))
DBDIR		:= $(addprefix $(DOCKERDIR)/, $(DB))
ENV_FILE	:= .env


DEPDIR			:= $(DBDIR)
DOCKERFILE		:= Dockerfile
DEPFILES		:= $(addsuffix /$(DOCKERFILE), $(DEPDIR) )

VOLUME_DB			:= mariadb_volume
VOLUME_WP			:= wordpress_volume
NETWORK				:= inception_net


all:
	@make $(NAME)

stop:
	docker container rm --force $(DB)  &>/dev/null
	docker container rm --force $(NGINX) &>/dev/null

clean:
	@make stop
	docker image rm $(DB) &>/dev/null
	docker image rm $(NGINX) &>/dev/null

fclean:
	@make clean
	docker volume rm $(VOLUME_DB) &>/dev/null
	docker volume rm $(VOLUME_WP) &>/dev/null
	docker network rm $(NETWORK) &>/dev/null

re:
	@make fclean
	@make $(NAME)

init:
	cp /etc/hosts /etc/hosts.bk
	sed -i "s/127.0.0.1/#127.0.0.1/" /etc/hosts
	echo "127.0.0.1 hsano.42.fr" >> /etc/hosts
	chmod 666 /var/run/docker.sock

dev:
	#@rm $(DJANGODIR)/root_static/*
	sed -i "s/DEBUG\s*=\s*False/DEBUG = True/" $(DJANGO_SETTING)
	sed -i "s/django.core.cache.backends.locmem.LocMemCache/django.core.cache.backends.dummy.DummyCache/" $(DJANGO_SETTING)
	python ft_trans/manage.py runserver


update:
	docker-compose -f docker/docker-compose.yml up -d --build

$(NAME): $(DEPFILES)
	#-@rm $(DJANGO_STATIC_DIR)/static/*
	-mkdir -p $(DJANGO_STATIC_DIR)/media
	-mkdir -p $(DJANGO_STATIC_DIR)/static
	sed -i	"s/DEBUG\s*=\s*True/DEBUG = False/" $(DJANGO_SETTING)
	sed -i	"s/django.core.cache.backends.dummy.DummyCache/django.core.cache.backends.locmem.LocMemCache/" $(DJANGO_SETTING)
	#docker-compose --env-file .env -f docker/docker-compose.yml up -d
	docker-compose   --env-file $(ENV_FILE)  -f docker/docker-compose.yml up -d

stop:
	docker-compose -f docker/docker-compose.yml down

.PHONY: all clean fclean re stop dev 
