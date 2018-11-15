FROM python:3.6
MAINTAINER Ihor Kuzmenko "0585ec@gmail.com"

ENV PYTHONUNBUFFERED 1

# setup
RUN apt-get update -q -y

RUN mkdir /mitra
WORKDIR /mitra
ADD . .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements/base.txt

EXPOSE 8000
EXPOSE 5432
EXPOSE 5672
