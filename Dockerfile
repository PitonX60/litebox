FROM python:3.8.6-slim

ENV PROJECT_NAME proj
ENV PROJECT_PATH /app
ENV FIREBIRD /opt/firebird

RUN apt update \
	&& apt install --no-install-recommends -y \
        wget gcc binutils ssh vim build-essential libfbclient2 \
	&& apt-get clean

RUN mkdir -p $PROJECT_PATH
WORKDIR $PROJECT_PATH

ADD requirements.txt $PROJECT_PATH
RUN pip3 install --use-feature=2020-resolver -r requirements.txt
RUN pip3 install --use-feature=2020-resolver https://github.com/maxirobaina/django-firebird/archive/stable/2.2.x.zip

ADD . $PROJECT_PATH

VOLUME $PROJECT_PATH/media
VOLUME $PROJECT_PATH/static

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
