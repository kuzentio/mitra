FROM python:3.5
MAINTAINER Ihor Kuzmenko "0585ec@gmail.com"

ENV PYTHONUNBUFFERED 1

# setup
RUN apt-get update -q -y

RUN mkdir /mitra
WORKDIR /mitra
ADD . .

RUN pip3 install --upgrade pip
