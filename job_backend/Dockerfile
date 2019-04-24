FROM ubuntu:19.04
FROM python:3.7.3-stretch
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "celery", "-A", "scrape_tasks", "worker", "--loglevel=INFO" ]