FROM python:3.11
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt install -y iproute2
RUN apt install -y python3-magic
WORKDIR /app
ADD requirements/production.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD main.py main.py
ADD src src