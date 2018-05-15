FROM python:3.6.3-alpine
RUN apk add --update \
    build-base \
    && rm -rf /var/cache/apk/*
ADD ./requirements.txt /
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV PYTHONUNBUFFERED 1