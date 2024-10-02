FROM python:3.9
RUN apt update
RUN apt install python3-magic
WORKDIR /app
ADD requirements/production.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD main.py main.py
ADD src src