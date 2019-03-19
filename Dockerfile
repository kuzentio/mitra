FROM python:3.6
MAINTAINER Ihor Kuzmenko "0585ec@gmail.com"

ENV PYTHONUNBUFFERED 1

# Install base dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y -q --no-install-recommends \
        apt-transport-https \
        build-essential \
        ca-certificates \
        curl \
        git \
        libssl-dev \
        python \
        rsync \
        software-properties-common \
        devscripts \
        autoconf \
        ssl-cert \
    && apt-get clean

# update the repository sources list
# and install dependencies
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install -y nodejs

# confirm installation
RUN node -v
RUN npm -v

# Use latest npm
RUN npm i npm@latest -g

RUN mkdir /mitra
WORKDIR /mitra
ADD . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/base.txt

EXPOSE 8088
EXPOSE 5432
EXPOSE 5000
EXPOSE 5672
EXPOSE 7000-7500
