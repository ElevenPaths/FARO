FROM ubuntu:focal as base
ARG BUILD_FARO_SRC_PATH
ARG TIKA_PORT
RUN apt-get update

ENV FARO_VERSION=2.0.0
MAINTAINER innovationlab@11paths.com

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip \
    locales bash parallel wget curl

RUN pip3 install --upgrade pip && \
    pip3 install nose coverage nosexcover \
    pylint unittest-xml-reporting==2.5.1

# Add dockerize to faro
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV LANG C.UTF-8

# Pass path to faro source code by argument
COPY ${BUILD_FARO_SRC_PATH}/requirements.txt /

RUN pip3 install -r /requirements.txt

COPY ./docker/Dockerfiles/faro/commands/* /entrypoint/commands/

WORKDIR /entrypoint/commands/

RUN ln -s /usr/bin/python3 /usr/bin/python

# Pass tika port as argument
ENV TIKA_PORT=$TIKA_PORT

ENTRYPOINT ["/bin/bash"]
