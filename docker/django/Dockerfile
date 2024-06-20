FROM python:3.11.9-slim-bullseye
MAINTAINER hsano hsano@student.42tokyo.jp
RUN apt update && apt upgrade -y
RUN apt install gettext -y

# 静的ファイルの配置(STATIC_ROOTディレクトリに移動)
WORKDIR /workspace

COPY ./.env /workspace
RUN python -m pip install --upgrade pip
RUN python -m pip install django-cors-headers
RUN python -m pip install Django==5.0.6
RUN python -m pip install daphne

#RUN python manage.py collectstatic

#COPY ./entrypoint.sh /workspace/entrypoint.sh
#ENTRYPOINT ["/workspace/entrypoint.sh"]
